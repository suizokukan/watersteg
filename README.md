# watersteg
GPLv3 / Python2|3 / Linux : apply a watermark to an image and steghide.

        Use this Python2/3 script in a Linux environment to apply some
        transformations (watermark + steghide) to an image.

        External programs required by watersteg :

        o ImageMagick (http://www.imagemagick.org/script/index.php)
        o Steghide (http://steghide.sourceforge.net/)

        Usage (see arguments below) :
        $ watersteg.py --help
        $ watersteg.py --source IMG_4280.JPG --passphrase="secret phrase" --message="Hello !"

        If you want to check what's written in your steghide'd image :
        $ steghide extract -sf picture_steghide.jpg

        NB : the destination path must exist otherwise an error will be raised.

#  transformations :

        (1) the original image is resized, watermarked and steghide'd.

                o function transform1__r400_wm_s()
                o (resize 400x... + watermark + steghide)
                o the watermark is a text added at several places on the
                  image.
                o new file name : FILENAME__TRANS1

        (2) the original image is steghide'd.

                o function transform2__steghide()
                o new file name : FILENAME__TRANS2
    
#   arguments :

  -h, --help            show this help message and exit

  --version             show the version and exit

  --source SOURCE
                        input file (default: None)

  --destpath DESTPATH
                        output path (default: .)

  --debug {True,False}  display debug messages (default: False)

  --passphrase PASSPHRASE
                        steghide passphrase (default: passphrase)

  --message MESSAGE     steghide message to be embed (default: message)

  --quiet {True,False}  disallow common messages' display; only the error
                        messages will be display (default: False)
    
#  history :

        o version 1 (2015_08_25)

                o initial version, pylint:10

        o version 2 (2015_08_25)

                o --version argument;
                o improve the messages display when the files are being created.

        o version 3 (2015_08_25)

                o if the outpath doesn't exist, the program exits;
                o INPUTFILE > SOURCE, --inputfile > --source
                o OUTPATH > DESTPATH, --outputpath > --destpath;
                o temporary files are now created by calling tempfile.NamedTemporaryFile()
                o the target files' name are defined at the beginning of the process;
                o improved the documentation;

# return value/error messages

        o no error value is returned.
        o error messages begin with "... !!", normal messages with "..." .
        o the --quiet option turns off normal messages, not the error ones.
          the --debug option turns on debug messages and has no effect on the normal
          or the error ones.