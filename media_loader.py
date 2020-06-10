# pylint: skip-file
# TODO: Fix lint

"""Media loading module.

Disclaimer:
    This is for technology demo purposes only of redflag.ai module. Not
    intended for production and commercial usage. In order to incorporate
    production and commercial use, integrate official APIs for
    corresponding platforms.
"""

import pathlib
import os
import datetime
import urllib.request
import youtube_dl

class MediaLoader:
    """Image, mp3, mp4 loading.

    Features:
    - Download mp3 from URL if video or audio present on the page
    - Download mp4 from URL if video or audio present on the page
    - Download image from URL if image present on the page
    """

    @staticmethod
    def image_directly(url, filepath):
        """Download image file from URL.

        Args:
        url -- str
            Direct URL to the image to download
        filepath -- str
            Path with filename to where save the downloaded file

        Return: bool
            True if media downloaded otherwise False.
        """
        try:
            urllib.request.urlretrieve(url, filepath)
            return filepath
        except: #pylint: disable=bare-except
            return None

    @staticmethod
    def image(url, filepath):
        """Download image file from URL.

        Args:
        url -- str
            URL of the page where to search for images
        filepath -- str
            Path with filename to where save the downloaded file

        Return: bool
            True if media downloaded otherwise False.
        """
        path = pathlib.Path(filepath)

        try:
            downloader = youtube_dl.YoutubeDL({
                'outtmpl': str(path)
            })

            downloader.download([url])

            return True
        except youtube_dl.utils.DownloadError as error:
            print(error)
            MediaLoader._remove_garbage(path)

            return False

    @staticmethod
    def mp4(url, filepath, limit=240, partial=False, savvy=False):
        """Download and convert to mp4 file from URL.

        Supports videos and gifs.

        Args:
        url -- str
            URL of the page where to search for video, gif, or audio tracks
        filepath -- str
            Path with filename to where save the downloaded file
        limit -- int, default=240
            Download only part of the video. Length of video to download
            in seconds. `partial` must be True for this to work
        partial -- bool, default=True
            If True, will use `limit` to download only beginning part of the
            video; otherwise, will proceed to full video length download

        Return: bool
            True if media downloaded otherwise False.
        """
        if partial and not MediaLoader._is_gif(url):
            return MediaLoader._download_partial_media(
                url,
                filepath,
                limit
            )

        return MediaLoader._download_media(url, filepath, 'mp4', savvy=savvy)

    @staticmethod
    def mp3(url, filepath):
        """Download and convert to mp3 file from URL.

        Args:
        url -- str
            URL of the page where to search for video or audio tracks
        filepath -- str
            Path with filename to where save the downloaded file

        Return: bool
            True if video downloaded and has audio track, otherwise False.
        """
        return MediaLoader._download_media(url, filepath, 'mp3')

    @staticmethod
    def _download_partial_media(url, filepath, limit):
        path = pathlib.Path(filepath)
        limit = str(datetime.timedelta(seconds=limit))

        output_code = os.system(
            f'ffmpeg $(youtube-dl -g "{url}" | '
            f'sed "s/.*/-ss 00:00 -i &/") -t {limit} -c copy {path}'
        )

        success = output_code == 0

        if not success:
            MediaLoader._remove_garbage(path)

        return success


    @staticmethod
    def _download_media(url, filepath, fileext, savvy=False):
        path = pathlib.Path(filepath)

        try:
            last_config = {}

            exec(os.environ.get('EXTRA_CONFIG', 'locals()["extra_config"] = {}'))

            if savvy:
                last_config['format'] = MediaLoader._get_small_format_code(url)

            downloader = youtube_dl.YoutubeDL({
                'cachedir': False,
                'outtmpl': f'{path.with_suffix("")}.%(ext)s',
                'postprocessors': [
                    # {
                    #     'key': 'FFmpegExtractAudio'
                    # },
                    {
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': fileext
                    }
                ],
                **locals()["extra_config"],
                **last_config
            })

            downloader.download([url])

            return True
        except youtube_dl.utils.DownloadError as error:
            print(error)
            MediaLoader._remove_garbage(path)

            return False

    @staticmethod
    def _remove_garbage(path):
        name_wo_suffix = path.with_suffix('').name
        for garbage_path in path.parent.glob(f'{name_wo_suffix}.*'):
            if garbage_path != path:
                garbage_path.unlink()
                print(f'Removed garbage: {garbage_path}')

    @staticmethod
    def _get_small_format_code(url):
        r = os.popen(f'youtube-dl -F "{url}"').read()
        ros = [(rr.split()[0], rr.split()[1]) for rr in r.split('\n') if any(rr) and not (rr.startswith('[') or rr.startswith('format code') or rr.find('audio only') != -1) and float(rr.split()[2].split('x')[1]) <= 480.0]
        ro = [rr1 for rr1, rr2 in ros if rr2 == 'mp4']
        return ro[-1] if any(ro) else ros[-1][0]


    @staticmethod
    def _is_gif(url):
        real_url = os.popen(f'youtube-dl -g "{url}"').read().strip()
        return real_url.endswith('.gif')
