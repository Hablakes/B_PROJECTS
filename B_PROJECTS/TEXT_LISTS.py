import os

movies_dir = os.listdir(r"/run/user/1000/gvfs/smb-share:server=10.0.0.3,share=bx-movies/MOVIES/")
tv_dir = os.listdir(r"/run/user/1000/gvfs/smb-share:server=10.0.0.3,share=bx-tv/TV/")
tv2_dir = os.listdir(r"/run/user/1000/gvfs/smb-share:server=10.0.0.3,share=bx-tv-2/TV-2/")


def create_movie_txt_file():
    with open('MOVIES.txt', 'w') as f:
        for movie_title in sorted(movies_dir):
            f.write("%s\n" % movie_title)


def create_tv_txt_file():
    with open('TV.txt', 'w') as f:
        for tv_title in sorted(tv_dir):
            f.write("%s\n" % tv_title)


def create_tv2_txt_file():
    with open('TV2.txt', 'w') as f:
        for tv_title in sorted(tv2_dir):
            f.write("%s\n" % tv_title)


create_movie_txt_file()
create_tv_txt_file()
create_tv2_txt_file()
