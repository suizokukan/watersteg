# Watersteg project : apply a watermark and some steganographic data in an image file.

     Use this Python2/3 script in a Linux environment to apply some
     transformations (watermark + steghide) to an image or a group of images.

     External programs required by watersteg :

         o ImageMagick (http://www.imagemagick.org/script/index.php)
         o Steghide (http://steghide.sourceforge.net/)

# Usage (see detailed arguments below) :

        $ watersteg.py --source "img/IMG_4280.JPG" --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        $ watersteg.py --source path/ --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        $ watersteg.py --source path/*.jpg --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        NB : the destination path must exist.


        If you want to check what's written in a steghide'd image(s) :

        $ steghide extract -sf picture_steghide.jpg

# Transformations :

        (1) the original image is resized, watermarked and steghide'd.

                o function transform1__r400_wm_s()
                o (resize 400x... + watermark + steghide)
                o the watermark is a text added at several places on the
                  image.
                o new file name : see FILENAME__TRANS1__FORMAT

        (2) the original image is steghide'd.

                o function transform2__steghide()
                o new file name : see FILENAME__TRANS2__FORMAT

        (3) the original image is steghide'd with an overlay placed over it

                o function transform3__steghide_overlay()
                o new file name : see FILENAME__TRANS3__FORMAT

        (4) the original image is written in gray and is steghide'd.

                o function transform2__steghide()
                o new file name : see FILENAME__TRANS4__FORMAT

        (5) the original image is written in gray, steghide'd and an overlay is put over.

                o function transform3__steghide_overlay()
                o new file name : see FILENAME__TRANS5__FORMAT
    
# Arguments :

  Arguments :

    usage: watersteg.py [-h] [--version] --source SOURCE [--destpath DESTPATH]
                        [--debug] --passphrase PASSPHRASE --message MESSAGE
                        [--quiet] --overlay OVERLAY

    optional arguments:
      -h, --help            show this help message and exit
      --version             show the version and exit
      --source SOURCE       input file or input directory. Wildcards accepted
                            (default: None)
      --destpath DESTPATH   output path (default: .)
      --debug               display debug messages (default: False)
      --passphrase PASSPHRASE
                            steghide passphrase (default: passphrase)
      --message MESSAGE     steghide message to be embed (default: message)
      --quiet               disallow common messages' display; only the error
                            messages will be display (default: False)
      --overlay OVERLAY     Overlay file to be used. (default: None)
   
# History :

        o version 6 (2015_10_25)

                o added a fifth transformation : transf5__gray__steg_overlay()
                o added a fourth transformation : transform4__gray__steghide()
                o added a call to os.path.expanduser() to developp ~ character.

                o fixed the transformation #3 : steghide is now the last step.
                o improved various messages

        o version 5 (2015_10_06)

                o added a third transformation : transform3__steghide_overlay()
                o raw Pylint : 10

        o version 4 (2015_08_03)

                o --source can be a path or a filename; the wildcards are accepted;
                o --quiet and --debug are now standalone options (no --quiet=True
                  anymore !)
                o an error is raised if the source is a file and if it doesn't exist;
                o improved the documentation;
                o raw Pylint : 10

        o version 3 (2015_08_25)

                o if the outpath doesn't exist, the program exits;
                o INPUTFILE > SOURCE, --inputfile > --source
                o OUTPATH > DESTPATH, --outputpath > --destpath;
                o temporary files are now created by calling tempfile.NamedTemporaryFile()
                o the target files' name are defined at the beginning of the process;
                o improved the documentation;
                o raw Pylint : 10

        o version 2 (2015_08_25)

                o --version argument;
                o improve the messages display when the files are being created.
                o raw Pylint : 10

        o version 1 (2015_08_25)

                o initial version, pylint:10

# return value/error messages

        o no error value is returned.
        o error messages begin with PROMPT + " !!", normal messages with the PROMPT .
        o debug messages begin with "@@" .
        o the --quiet option turns off normal messages, not the error ones.
          the --debug option turns on debug messages and has no effect on the normal
          messages or on the error ones.