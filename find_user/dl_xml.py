import sys
import requests


def dl_xml(cid):
    url_head = "http://comment.bilibili.com/"
    file_name = cid + ".xml"
    url = url_head + file_name
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("check your cid")
        raise SystemExit(err)
    open(f"./{file_name}", "wb").write(r.content)
    print(f"successful! file saved as {file_name}")


if __name__ == "__main__":
    cid = sys.argv[1]
    dl_xml(cid)
