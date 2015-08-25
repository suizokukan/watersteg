# watersteg
GPLv3 / Python2|3 / Linux : apply a watermark to an image and steghide.

        Use this Python2/3 script in a Linux environment to apply some
        transformations (watermark + steghide) to an image.

        External programs required by watersteg :

        o ImageMagick (http://www.imagemagick.org/script/index.php)
        o Steghide (http://steghide.sourceforge.net/)

        Usage (see arguments below) :
        $ watersteg.py --help
        $ watersteg.py --inputfile IMG_4280.JPG --passphrase="secret pass" --message="Hello !"

# transformations :

        (1) the original image is resized, watermarked and steghide'd.

                (resize 400x... + watermark + steghide)

                The watermark is a text added at several places on the
                image.

                new file name : FILENAME__TRANS1

        (1) the original image is steghide'd.

                new file name : FILENAME__TRANS2

# arguments :

  -h, --help            show this help message and exit

  --inputfile INPUTFILE
                        input file (default: None)

  --outputpath OUTPUTPATH
                        output path (default: .)

  --debug {True,False}  display debug messages (default: False)

  --passphrase PASSPHRASE
                        steghide passphrase (default: passphrase)

  --message MESSAGE     steghide message to be embed (default: message)

  --quiet {True,False}  disallow common messages' display; only the error
                        messages will be display (default: False)
# history :

        o version 1 (2015_08_25)

                initial version, pylint:10
    
