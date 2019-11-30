import json
import requests
from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from get_lilic import serializers
import re

# Create your views here.
class GetLilicApiView(APIView):
    serializer_class = serializers.LilicSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            music_name = serializer.validated_data.get('music_name')
            artist_name = serializer.validated_data.get('artist_name')
            lilic = get_lilic(music_name,artist_name)
            return Response({'lilic':lilic})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )



async def get_lilic_url(music_name, artist_name):
    browser = await launch(headless=True,handleSIGINT=False,
    handleSIGTERM=False,
    handleSIGHUP=False)
    page = await browser.newPage()
    await page.goto('http://j-lyric.net/')
    await page.type('#keyword',music_name)
    await page.waitFor(800);
    await page.click('input[type=submit]')
    await page.waitFor(700);
    await page.click('a[title*="' + artist_name + '"]')
    await page.waitFor(500);
    html = await page.content()
    url1 = page.url
    await browser.close()
    return url1


def get_lilic(music_name,artist_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        url = loop.run_until_complete(get_lilic_url(music_name,artist_name))
    finally:
        loop.close()
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    bs = BeautifulSoup(response.text, 'html.parser')
    lilic = ""
    for t in bs.select("#Lyric"):
        lilic += t.get_text()
    return lilic
