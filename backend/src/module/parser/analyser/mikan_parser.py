import re
import logging

from bs4 import BeautifulSoup
from urllib3.util import parse_url

from module.network import RequestContent
from module.utils import save_image

logger = logging.getLogger(__name__)

def mikan_parser(homepage: str):
    root_path = parse_url(homepage).host
    with RequestContent() as req:
        content = req.get_html(homepage)
        soup = BeautifulSoup(content, "html.parser")
        
        poster_div_el = soup.find("div", {"class": "bangumi-poster"})
        poster_div = poster_div_el.get("style") if poster_div_el else None
        
        official_title_el = soup.select_one(
            'p.bangumi-title a[href^="/Home/Bangumi/"]'
        )
        if not official_title_el:
            logger.warning(f"Failed to parse title for homepage: {homepage}")
            return "", ""
            
        official_title = official_title_el.text
        official_title = re.sub(r"第.*季", "", official_title).strip()
        
        if poster_div:
            try:
                poster_path = poster_div.split("url('")[1].split("')")[0]
                poster_path = poster_path.split("?")[0]
                img_url = f"https://{root_path}{poster_path}"
                img = req.get_content(img_url)
                
                if img:
                    suffix = poster_path.split(".")[-1]
                    poster_link = save_image(img, suffix)
                    return poster_link, official_title
                else:
                    logger.warning(f"Failed to download image: {img_url}")
            except Exception as e:
                logger.error(f"Failed to parse poster for {homepage}: {e}")
                
        return "", official_title


if __name__ == '__main__':
    homepage = "https://mikanani.me/Home/Episode/c89b3c6f0c1c0567a618f5288b853823c87a9862"
    print(mikan_parser(homepage))
