Import("env")

env.Replace(
    UPLOADER="$PYTHONEXE",
    UPLOADERFLAGS= [
        "-u", # unbuffered, makes output appear
        "\"$PROJECT_DIR/esplink_upload.py\""
        # "-P IP" and "-b baud" auto added by a "BeforeUpload" action in platform-atmelavr
    ],
    UPLOADCMD="\"$UPLOADER\" $UPLOADERFLAGS $SOURCES",
)
