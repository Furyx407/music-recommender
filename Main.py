''' This Will Try To Use Dependencies, 
yt_dlp to get playlist information,
bs4 / BeautifulSoup and requests to get the video tags
lingua for language detection, (kinda overkill but...)
re and urllib to search youtube'''
try:
# Import Dependencies	
    import yt_dlp
    from bs4 import BeautifulSoup
    import requests
    from lingua import Language, LanguageDetectorBuilder
    from re import findall
    from urllib.request import urlopen
    from time import sleep

#If it is unable to use any
except ImportError: 
    print("Missing dependencies, please install them with 'pip install -r requirements.txt'")
    exit(1)
'''
error codes
 1 = dependencies are missing
 2 = user exit
 3 = Error with Variable setup
 57 = ytdl failure
'''

'''These are most of the variables, some I couldn't put in for some reasons or another (Unknown output format is main cause)
Some are global because I chose to put stuff into functions after instead of properly planning. It was not designed to be modular but I made it kinda...
    '''
# In a "Try" mainly because it shortens it XD
try:
    #  Variables

    # Test link (for startup test) CAN CHANGE
    tstlink = "https://www.youtube.com/watch?v=FtutLA63Cp8"

    #Playlist link
    lst = ""

    #list of videos
    Vid_list = []

    ''' These Variables Are For / Related To Tags '''
    # tags
    tgs = []
    # Combined Tags
    global cmbtgs
    cmbtgs = []
    # Filtered tags (after combined)
    global ftgs
    ftgs: dict[str, int] = {}
    # applied filtered tags
    aftg = []
    remftg = []
    # Lyrics in top 5
    litf:bool = False
    # Combined top 5
    global cmbtkey
    cmbtkey:str = ""
    # Temp cache for tags
    metatag = []

    # Video information
    title = ""
    video_id = ""
    tags = ""
    video_url = ""

    # Temp cache for keywords
    keywords = []
    # top keywords
    global tkey
    tkey = []


    #recommended output
    recvid = []
    ytout = []
    ftout = []
    fftout = []
    recarray = []
    rectitle = []
    recurl = []

    #settings
    # Video download toggle
    global vidtog
    vidtog:bool = False
    global viddisp
    viddisp:str = "OFF"
    #Auto send to login screen
    global autores
    autores:bool = False
    global autoresdisp
    autoresdisp:str = "OFF"

    
    # Intro / Dialog screens
    global logo
    logo = r"""
        ┌────────────────────────────────────────────────────────────────────┐  
        │ __  __           _                                                 │  
        │|  \/  |_   _ ___(_) ___                                            │  
        │| |\/| | | | / __| |/ __|                                           │  
        │| |  | | |_| \__ \ | (__                                            │  
        │|_|__|_|\__,_|___/_|\___|                               _           │  
        │|  _ \ ___  ___ ___  _ __ ___  _ __ ___   ___ _ __   __| | ___ _ __ │  
        │| |_) / _ \/ __/ _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \ / _` |/ _ \ '__|│  
        │|  _ <  __/ (_| (_) | | | | | | | | | | |  __/ | | | (_| |  __/ |   │  
        │|_| \_\___|\___\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__,_|\___|_|   │  
        └────────────────────────────────────────────────────────────────────┘  
    """

    # Show options for the intro screen
    global opt
    opt = f"""
     1. Recommend video based off playlist 
     2. Settings 
     3. Exit"""

    # Show options for settings
    
except KeyboardInterrupt:
    exit(2)
except:
    print("There was an error with the Variables")
    exit(3)

# Self explanitory, controls main introduction screen
def intro(vidtog, viddisp, autores, autoresdisp):
    while True:
        print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(logo)
        print(f"\n\n\n\n\n")
        print(opt)
        intrs = input("Select 1-3:  ")
        if intrs == "1":
            print(f"\n\n\n")
            getplaylist()
            playlist_info,keywords,tgs,Vid_list = Vidfetch(lst)
            #tagproc(tgs)
            break
        elif intrs == "2":
            vidtog , viddisp , autores , autoresdisp = settings(vidtog,viddisp,autores,autoresdisp)
        elif intrs == "3":
            exit(2)
    return(vidtog, viddisp, autores, autoresdisp)

# Settings menu
def settings(vidtog,viddisp,autores,autoresdisp):
    sop = f"""
        1. Set Recommended Video Download ( ON / OFF ) {viddisp}
        2. Set Auto Return ( ON / OFF ) {autoresdisp}
        3. Back
        """
    print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(logo)
    print(f"\n\n\n\n\n")
    print(sop)

    srs = input("Select 1-3:    ")
    sop = f"""
    1. Set Recommended Video Download ( ON / OFF ) {viddisp}
    2. Set Auto Return ( ON / OFF ) {autoresdisp}
    3. Back
    """
    if srs == "1":
        togd = input("Set recommended video download ( ON / OFF ) : ")
        if togd.lower() == "on":
            vidtog = True
            viddisp = "ON"
            print("Recommended video download set to ON")
        elif togd.lower() == "off":
            vidtog = False
            viddisp = "OFF"
            print("Recommended video download set to OFF")
        else:
            print("Invalid input, please try again")
        vidtog,viddisp,autores,autoresdisp = settings(vidtog,viddisp,autores,autoresdisp)
    elif srs == "2":
        togr = input("Set Auto Return ( ON / OFF ) : ")
        if togr.lower() == "on":
            autores = True
            autoresdisp = "ON"
        elif togr.lower() == "off":
            autores = False
            autoresdisp = "OFF"
        vidtog,viddisp,autores,autoresdisp = settings(vidtog,viddisp,autores,autoresdisp)
            
    elif srs == "3":
        vidtog, viddisp, autores, autoresdisp = intro(vidtog, viddisp, autores, autoresdisp)
    else:
        print("Invalid input, please try again")
        vidtog,viddisp,autores,autoresdisp = settings(vidtog,viddisp,autores,autoresdisp)
    return(vidtog ,viddisp ,autores ,autoresdisp )
    

# Responsible for getting link of playlist / mix
def getplaylist():
    # Get the playlist link
    global lst
    while True:
        print("Paste in youtube playlist (or mix) link below")
        lst = input("INPUT PLAYLIST (OR MIX) : ")
    # Use https://www.youtube.com/playlist?list=PLStNb4D3dWAoYBNM3IQXENoTK7UbpIlPQ for testing
    # POP: https://www.youtube.com/playlist?list=PLDIoUOhQQPlXqz5QZ3dx-lh_p6RcPeKjv
    # MIX, VERY LONG: https://www.youtube.com/watch?v=Kr2lbQwHQeY&list=RDMMKr2lbQwHQeY&start_radio=1&pp=0gcJCfoCOCosWNin

        # Check if actual playlist or mix link
        if lst.startswith("https://www.youtube.com/playlist?list=" ):
            break
        elif lst.startswith("https://www.youtube.com/") and "&list=" in lst:
            break
        else:
            print("\n \n Please Paste a PLAYLIST link below, it starts with https://www.youtube.com/playlist?list=  \n \n OR put in a link for a mix, that starts with ' https://www.youtube.com/watch? ' and has ' &list= ' in the URL \n")
    # Sends playlist link into function called Vidfetch
    return(lst)

# Gets information of videos from the playlist link, passes tags to tagproc function
def Vidfetch(playlist_link):
    global tgs
    global tkey
    tkey = []
    # Config for youtube-dlp
    ydlp_opt = {
            'extract_flat': True,
            'skip_download': True,
    }

    # Get info about playlist
    global playlist_info
    with yt_dlp.YoutubeDL(ydlp_opt) as ytdl:
        playlist_info = ytdl.extract_info(playlist_link, download=False)

    print("Videos Fetched \n")

    if not 'entries' in playlist_info:
        return("Nothing in playlist")
    
    print(f"Playlist Name: {playlist_info.get('title')}\n")

    for video in playlist_info['entries']:
        try:
            # Assigns title, id, tags and url to temp variables
            title = video.get('title')
            video_id = video.get('id')
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            Vid_list.append([title,video_id,video_url])

            print(f"Video Title : {title}")
            print(f"URL : {video_url}")
            try:
                vid = requests.get(video_url)
                metatag = BeautifulSoup(vid.content, 'html.parser').select_one("meta[name=keywords]")
        # If there are tags
                if metatag:
                    keywords = metatag["content"].split(",")
                    tgs.append(keywords)
            except ConnectionError:
                print("Connection Error")
            except KeyboardInterrupt:
                exit()
            print(f"Keywords : {keywords} \n")
        except KeyboardInterrupt:
            exit
    tkey,ftgs,cmbtkey = tagproc(tgs,tkey)

    return (playlist_info,keywords,tgs,Vid_list)

# This Takes the combined tags from tagproc and searches youtube for appropriate videos
def getvidresult(query:str, qarray:list):
    if query:
        print(query)
        sq = query.replace(", ", " ")
        print(sq)
        searchq = sq.replace(" ", ",")
    else:
        tmpstr = ""
        for i in qarray:
            tmpstr = tmpstr + ", " + i
        searchq = tmpstr
        print(searchq)
    print(f" SEARCH QUERY = {searchq}")
    html = urlopen(f"https://www.youtube.com/results?search_query={searchq}")
    print(" Extracting videos. May take a while...")

    video_id = findall(r"watch\?v=(\S{11})", html.read().decode())
    print(f"Video IDs: {video_id}")
    tmpint:int = 0
    for i in video_id:
        print(i)
        if i in video_id[tmpint-1]:
            pass
        else:
            if "&start_radio" in i:
                tmp = i.split("&start_radio")[0]
                ftout.append(tmp)
            else:
                tmp = i
                ftout.append(tmp)
            print(ftout)
            if "&list" in tmp:
                tmp2 = tmp.split("&list")[0]
                fftout.append(tmp2)
            else:
                tmp2 = tmp
                fftout.append(tmp2)
        yt_dlp_opt = {
                'extract_flat': True,   
                'skip_download': True
        }
        print(f"FT OUT \n\n {fftout} \n \n \n \n")
        for i in fftout:
            recarray.append(f"https://www.youtube.com/watch?v={i}")
        print(recarray)
        tmpint = tmpint + 1

    recurl = []
    for i in recarray[0:4]:
        try:
            with yt_dlp.YoutubeDL(yt_dlp_opt) as ytdl:
                tvid = ytdl.extract_info(i, download = False,)
                rectitle.append(tvid.get('title'))
                recurl = fftout
                recvid.append(tvid)
        except:
            print("Error incurred with getting Video Information")
    #print( ' \n \n \n return \n\n')
# print it !!!!!!
    return(recvid, rectitle, fftout, recurl)

#Tag processing
def tagproc(tgs,tkey):
        # Combined Tags
    cmbtgs = []
        # Attached Tags -- if alr included in list, get excluded. All in list are a fallback if it doesn't get properly filtered (Still not working)
    atgs = ['video','sharing','camera phone','video phone','free','upload']
        # To detect what language it is -- "Language Detection"
    landet=LanguageDetectorBuilder.from_all_languages().with_minimum_relative_distance(0.9).build()
        # loops for all entry groups in the tag list
    for entg in tgs:
            # separates the grouped tags bcus earlier formatting
        for entr in entg:
                # if has lyrics in keyword makes tag lyrics, if diff language then makes tag that language
            if "lyrics" in entr.lower() or "lyric" in entr.lower():
                entr = "lyrics"

                # If language detects nothing, keep tag
            elif str(landet.detect_language_of(entr)).removeprefix("Language.") == "None":
                entr = entr

                # If language decects other language, make tag name of language (not bothered for more processing)
            elif landet.detect_language_of(entr) != Language.ENGLISH:
                entr = str(landet.detect_language_of(entr)).removeprefix("Language.")
                entr = entr.replace(" ", "")
                # if not already in list
            if entr.lower() not in atgs:
                cmbtgs.append([entr.lower(),1])
                atgs.append(entr.lower())

                #if in list
            else:
                    # go through all options to see if it's there, then increase count
                for i in cmbtgs:
                    if i[0] == entr.lower():
                        ip1 = i[1]
                        i[1] = int(ip1) + 1
    cmbtgs = sorted(cmbtgs, key=lambda row:([len(str(ele)) for ele in row]))

    for i in cmbtgs:
                    # if it appears multiple times, compresses it
                for r in cmbtgs:
                    if i in r and i != r:
                        if not i[0] in ['free', 'video' , 'sharing', 'video phone', 'camera phone']:
                        
                            if i[0] not in aftg and i[0] not in aftg:
                                aftg.append(i[0])
                                remftg.append(r[0])
                                numir = int(i[0]) + int(r[0])
                                ftgs.update({str(i[0]):int(numir)})
                            else:
                                try:

                                    itf:str = i[0]
                                    for values,key in ftgs:
                                        if values == itf:
                                            numir = int(key) + int(r[1])
                                            ftgs[itf] = int(numir)
        
                                except ValueError:
                                    print("val error")
        
                    if i[0] not in aftg and i[0] not in remftg:
                        ftgs.update({str(i[0]):int(i[1])})

    # Sort tags by how often the occured, (Least to most)
    cmbtgs.sort(key=lambda x: x[1])
    # Sort the filtered tags by how often ( Most to least)
    global sftgs
    sftgs = sorted(ftgs.items(), key=lambda x: x[1], reverse=True)
    litf:bool = False
    for i in range(5):
        if "lyrics" in sftgs[i-1]:
            litf = True
            break
    #tkey = []
    if litf:
        tkey = sftgs[:5]
        for i in tkey:
            if "lyrics" in i:
                tkey.remove(i)
            else:
                tkey = sftgs[:4]
    cmbtkey = ""
    for i in tkey:
        if " " in i[0]:
            cmbtkey += i[0]
        cmbtkey += ", " + i[0]
    print(cmbtkey)
    recvid, rectitle, fftout, recurl = getvidresult(cmbtkey, tkey)
    #print("\n\n\n\n\n\n\n\n\n FINISHED GETVIDRES \n\n\n\n\n\n")
    printres(rectitle,recurl)
    return(tkey,ftgs,cmbtkey)

def printres(titles:list,urls:list):
# If the playlist is not empty
    Vid_len = len(Vid_list)
    # Prints info
    print(f"Playlist: {playlist_info.get('title')}")
    # if not empty
    if Vid_len != 0:
        print(f"{Vid_len} videos found")
    else:
        print("No videos found :(")
    # if there are tags
    if tgs != []:
        # Process the tags
        #tagproc()
        print(f"Keywords Found: {len(ftgs)} \n")

        print(f"\n \n \n Top Keywords: {sorted(sftgs, key=lambda x: x[1], reverse=True)[:4]}")
    print("\n \n \n")

    #raise("not implemented", 35)
    if titles:
        print(f"\n\n\n\n\n Video Name: {titles[0]}")
    else:
        print(f"\n\n\n\n\n Video(s) Name: {titles}")
    if urls:
        print(f"Video URL: www.youtube.com/watch?v={urls[0]}\n\n")
    else:
        print(f"Video URL(s): www.youtube.com/watch?v={urls}\n\n")

    if vidtog:
        yt_opt = {
    'extract_flat': True,
    'skip_download': False,
}
        with yt_dlp.YoutubeDL(yt_opt) as ytdl:
            ytdl.download(str(f"www.youtube.com/watch?v={urls[0]}"))
    
    #print("\n\n DEBUG END \n\n")  
    if not autores:
        print("\nPress Enter to return to main menu\n OR type anything else to exit")
        if input() == "":
            pass
        else:
            exit(2)
    else:
        sleep(5)


  

    #raise("not implemented", 35)
        
# Main Code *
while True:
    vidtog, viddisp, autores, autoresdisp = intro(vidtog, viddisp, autores, autoresdisp)

    x = False
    if x:
        # If the playlist is not empty
        Vid_len = len(Vid_list)
        # Prints info
        print(f"Playlist: {playlist_info.get('title')}")
        # if not empty
        if Vid_len != 0:
            print(f"{Vid_len} videos found")
        else:
            print("No videos found :(")
        # if there are tags
        if tgs != []:
            # Process the tags
            #tagproc()
            print(f"Keywords Found: {len(ftgs)} \n")

            print(f"\n \n \n Top Keywords: {sorted(sftgs, key=lambda x: x[1], reverse=True)[:4]}")
        print("\n \n \n")
        if not autores:
                print("\nPress Enter to return to main menu\n OR type anything else to exit")
                if input() == "":
                    pass
                else:
                    exit(2)
        else:
            sleep(5)
