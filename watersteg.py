#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#    Watersteg Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Watersteg.
#    Watersteg is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Watersteg is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Watersteg.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
     Watersteg project : apply a watermark and some steganographic data in an
                         image file.

     Use this Python2/3 script in a Linux environment to apply some
     transformations (watermark + steghide) to an image or a group of images.

     External programs required by watersteg :
         o ImageMagick (http://www.imagemagick.org/script/index.php)
         o Steghide (http://steghide.sourceforge.net/)

  ______________________________________________________________________________

  Usage (see detailed arguments below) :

        $ watersteg.py --help

        $ watersteg.py --source "img/IMG_4280.JPG"
                       --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        $ watersteg.py --source path/
                       --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        $ watersteg.py --source path/*.jpg
                       --passphrase="secret phrase" --message="Hello !" --overlay="overlay.png"

        NB : the destination path must exist.


        If you want to check what's written in a steghide'd image(s) :

        $ steghide extract -sf picture_steghide.jpg
  ______________________________________________________________________________

  Transformations :

        (1) the original image is resized, watermarked and steghide'd.

                o function transform1__r400_wm_s()
                o (resize 400x... + watermark + steghide)
                o the watermark is a text added at several places on the
                  image.
                o new file name : see FILENAME__TRANS1__FORMAT

        (2) the original image is steghide'd.

                o function transform2__steghide()
                o new file name : see FILENAME__TRANS2__FORMAT

        (3) the original image is steghide'd and an overlay is put over.

                o function transform3__steghide_overlay()
                o new file name : see FILENAME__TRANS3__FORMAT

        (4) the original image is written in gray and is steghide'd.

                o function transform2__steghide()
                o new file name : see FILENAME__TRANS4__FORMAT

        (5) the original image is written in gray, steghide'd and an overlay is put over.

                o function transform3__steghide_overlay()
                o new file name : see FILENAME__TRANS5__FORMAT
  ______________________________________________________________________________

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
  ______________________________________________________________________________

  History :

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
  ______________________________________________________________________________

  return value/error messages

        o no error value is returned.
        o error messages begin with PROMPT + " !!", normal messages with the PROMPT .
        o debug messages begin with "@@" .
        o the --quiet option turns off normal messages, not the error ones.
          the --debug option turns on debug messages and has no effect on the normal
          or the error ones.
"""

import argparse
import fnmatch
import os.path
from subprocess import check_output
import sys
import tempfile

PROGRAM_VERSION = "6"
PROGRAM_NAME = "Watersteg"

# prompt displayed before any message on the console :
PROMPT = "~"

# file where the message to be embed will be written. This file will be erased
# (see the end of the file).
STEGHIDE__EMBED_FILE = "steghide.embed"

# format of the destination files :
#
#     o  {0} : DESTPATH
#     o  {1} : BASENAME
#     o  {2} : EXTENSION
#
FILENAME__TRANS1__FORMAT = "{0}{1}_1_400x_watermark_steghide{2}"
FILENAME__TRANS2__FORMAT = "{0}{1}_2_steghide{2}"
FILENAME__TRANS3__FORMAT = "{0}{1}_3_steghide_overlay{2}"
FILENAME__TRANS4__FORMAT = "{0}{1}_4_gray_steghide{2}"
FILENAME__TRANS5__FORMAT = "{0}{1}_5_gray_steghide_overlay{2}"

#///////////////////////////////////////////////////////////////////////////////
def system(order):
    """
        Give a system "order" through a call to os.system() .

        Display the order if an error occurs and stop the program.
    """
    if ARGS.debug:
        print("@@ os.system() : \"{0}\"".format(order))

    return os.system(order)

#///////////////////////////////////////////////////////////////////////////////
def external_programs_are_available():
    """
        Check that the external programs required by waterseg are present.
        If an error occurs, display a message explaining what was the problem.

        Return a boolean.
    """
    result = True

    with tempfile.NamedTemporaryFile(mode='w', delete='True') as tmpfile:

        # TEST : does "convert" exist ?
        if result and system("convert -version > {0}".format(tmpfile.name)) != 0:
            print("{0} !! ImageMagic/convert can't be find : " \
                  "the program has to stop.".format(PROMPT))
            result = False

        # TEST : does "steghide" exist ?
        if result and system("steghide --version > {0}".format(tmpfile.name)) != 0:
            print("{0} !! steghide can't be find : the program has to stop.".format(PROMPT))
            result = False

    return result

#///////////////////////////////////////////////////////////////////////////////
def get_args():
    """
        Read the command line arguments.

        Return the argparse object.
    """
    parser = argparse.ArgumentParser(description="{0} v. {1}".format(PROGRAM_NAME, PROGRAM_VERSION),
                                     epilog="by suizokukan AT orange DOT fr",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version',
                        action='version',
                        version="{0} v. {1}".format(PROGRAM_NAME, PROGRAM_VERSION),
                        help="show the version and exit")

    parser.add_argument('--source',
                        type=str,
                        required=True,
                        help="input file or input directory. Wildcards accepted")

    parser.add_argument('--destpath',
                        type=str,
                        default=".",
                        help="output path")

    parser.add_argument('--debug',
                        action="store_true",
                        help="display debug messages")

    parser.add_argument('--passphrase',
                        type=str,
                        required=True,
                        default="passphrase",
                        help="steghide passphrase")

    parser.add_argument('--message',
                        type=str,
                        required=True,
                        default="message",
                        help="steghide message to be embed")

    parser.add_argument('--quiet',
                        action="store_true",
                        help="disallow common messages' display; " \
                             "only the error messages will be display")

    parser.add_argument('--overlay',
                        type=str,
                        required=True,
                        help="Overlay file to be used.")

    return parser.parse_args()

#///////////////////////////////////////////////////////////////////////////////
def transform1__r400_wm_s(sourcefilename, destfilename):
    """
        transformation :

                source file -> source file + resize 400 + watermark + steghide

        this function should be only called by apply_transformations()
    """
    with tempfile.NamedTemporaryFile(mode='w', delete='True') as tmpfile:

        # resize 400x...
        system("convert \"{0}\" -resize 400 \"{1}\"".format(sourcefilename,
                                                            tmpfile.name))

        if not ARGS.quiet:
            print("     {0} ... creating {1} ...".format(PROMPT, destfilename))

        # watermark
        system("convert -size 240x160 xc:none -fill grey " \
               "-gravity NorthWest -draw \"text 10,10 '{2}'\" " \
               "-gravity SouthEast -draw \"text 5,15 '{2}'\" miff:- " \
               "| composite -tile - \"{0}\" \"{1}\"".format(tmpfile.name,
                                                            destfilename,
                                                            ARGS.message))

        # steghide
        system("steghide embed -cf \"{0}\" -ef \"{1}\" -p \"{2}\" -q".format(destfilename,
                                                                             STEGHIDE__EMBED_FILE,
                                                                             ARGS.passphrase))

#///////////////////////////////////////////////////////////////////////////////
def transform2__steghide(sourcefilename, destfilename):
    """
        transformation :

                source file -> source file + steghide

        this function should be only called by apply_transformations()
    """
    if not ARGS.quiet:
        print("     {0} ... creating {1} ....".format(PROMPT, destfilename))

    system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
           "-p \"{2}\" -q -sf \"{3}\" -f".format(sourcefilename,
                                                 STEGHIDE__EMBED_FILE,
                                                 ARGS.passphrase,
                                                 destfilename))

#///////////////////////////////////////////////////////////////////////////////
def transform3__steghide_overlay(sourcefilename, destfilename, overlay):
    """
        transformation :

                source file -> source file + steghide + overlay

        this function should be only called by apply_transformations()
    """
    if not ARGS.quiet:
        print("     {0} ... creating {1} ....".format(PROMPT, destfilename))

    # dimensions of the source file  ?
    size = check_output(["identify", "-format", "%wx%h", sourcefilename])

    system("convert -size {0} -composite \"{1}\" \"{2}\" " \
           "-geometry {0}+0+0 -depth 8 \"{3}\"".format(size.decode(),
                                                       sourcefilename,
                                                       overlay,
                                                       destfilename))

    system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
           "-p \"{2}\" -q -sf \"{3}\" -f".format(destfilename,
                                                 STEGHIDE__EMBED_FILE,
                                                 ARGS.passphrase,
                                                 destfilename))

#///////////////////////////////////////////////////////////////////////////////
def transform4__gray__steghide(sourcefilename, destfilename):
    """
        transformation :

                source file -> source file in gray + steghide

        this function should be only called by apply_transformations()
    """
    if not ARGS.quiet:
        print("     {0} ... creating {1} ....".format(PROMPT, destfilename))

    system("convert -grayscale rec709luma \"{0}\" \"{1}\"".format(sourcefilename,
                                                                  destfilename))

    system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
           "-p \"{2}\" -q -sf \"{3}\" -f".format(destfilename,
                                                 STEGHIDE__EMBED_FILE,
                                                 ARGS.passphrase,
                                                 destfilename))

#///////////////////////////////////////////////////////////////////////////////
def transf5__gray__steg_overlay(sourcefilename, destfilename, overlay):
    """
        transformation :

                source file -> source file + steghide + overlay

        this function should be only called by apply_transformations()
    """
    if not ARGS.quiet:
        print("     {0} ... creating {1} ....".format(PROMPT, destfilename))

    # dimensions of the source file  ?
    size = check_output(["identify", "-format", "%wx%h", sourcefilename])

    system("convert -grayscale rec709luma -size {0} -composite \"{1}\" \"{2}\" " \
           "-geometry {0}+0+0 -depth 8 \"{3}\"".format(size.decode(),
                                                       sourcefilename,
                                                       overlay,
                                                       destfilename))

    system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
           "-p \"{2}\" -q -sf \"{3}\" -f".format(destfilename,
                                                 STEGHIDE__EMBED_FILE,
                                                 ARGS.passphrase,
                                                 destfilename))

#///////////////////////////////////////////////////////////////////////////////
def apply_transformations(destination_path,
                          source_basename,
                          source_extension,
                          source_directory,
                          overlay):
    """
        Apply all defined transformations to the source_* file and write the
        resulting files in destination_path .
    """
    filename__trans1 = FILENAME__TRANS1__FORMAT.format(destination_path,
                                                       source_basename,
                                                       source_extension)
    transform1__r400_wm_s(source_directory, filename__trans1)


    filename__trans2 = FILENAME__TRANS2__FORMAT.format(destination_path,
                                                       source_basename,
                                                       source_extension)
    transform2__steghide(source_directory, filename__trans2)

    filename__trans3 = FILENAME__TRANS3__FORMAT.format(destination_path,
                                                       source_basename,
                                                       source_extension)
    transform3__steghide_overlay(source_directory, filename__trans3, overlay)

    filename__trans4 = FILENAME__TRANS4__FORMAT.format(destination_path,
                                                       source_basename,
                                                       source_extension)
    transform4__gray__steghide(source_directory, filename__trans4)

    filename__trans5 = FILENAME__TRANS5__FORMAT.format(destination_path,
                                                       source_basename,
                                                       source_extension)
    transf5__gray__steg_overlay(source_directory, filename__trans5, overlay)


#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
#///                                                                         ///
#///                            ENTRY POINT                                  ///
#///                                                                         ///
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
#
# (0) warm-up
#
#///////////////////////////////////////////////////////////////////////////////

# (0.a) arguments from the command line
ARGS = get_args()

# (0.b) source file/directory
SOURCE = os.path.expanduser(ARGS.source)

SOURCE_TYPE = None
if os.path.isfile(SOURCE):
    SOURCE_TYPE = "a file"
elif os.path.isdir(SOURCE):
    SOURCE_TYPE = "a directory"
else:
    # ... hopefully something with wildcards.
    SOURCE_TYPE = "neither a file nor a directory"

# (0.c) destination path
DESTPATH = os.path.expanduser(ARGS.destpath)
if not DESTPATH.endswith("/"):
    DESTPATH += "/"
if not os.path.exists(DESTPATH):
    print("{0} !! the destination path \"{1}\" doesn't exist : " \
          "the program has to stop.".format(PROMPT, DESTPATH))
    sys.exit()

# (0.d) overlay file
OVERLAY = os.path.expanduser(ARGS.overlay)

# (0.e) displaying the summary
if not ARGS.quiet:
    print("=== {0} v. {1} === ".format(PROGRAM_NAME, PROGRAM_VERSION))

    print("{0} source=\"{1}\" ({2})".format(PROMPT, SOURCE, SOURCE_TYPE))
    if SOURCE_TYPE == "neither a file nor a directory":
        print("{0} source \"{1}\" is neither an existing file nor an existing directory : " \
              "it will be analysed as a path with wildcards.".format(PROMPT, SOURCE))

    print("{0} output path=\"{1}\"".format(PROMPT, DESTPATH))

# (0.f) are the required external programs available ?
if not external_programs_are_available():
    sys.exit()

# (0.g) creating the embed file used by steghide :
with open(STEGHIDE__EMBED_FILE, "w") as steghide_message:
    steghide_message.write(ARGS.message)

#///////////////////////////////////////////////////////////////////////////////
#
# (1) transformations
#
#///////////////////////////////////////////////////////////////////////////////
NUMBER_OF_FILES_READ_AND_TRANSFORMED = 0

if SOURCE_TYPE == 'a file':
    # it's a file : let's read and transform it.

    # e.g. if SOURCE = img/IMG_4280.JPG,
    #           then SOURCE_BASENAME = IMG_4280.JPG
    #           then SOURCE_EXTENSION = .JPG
    SOURCE_BASENAME, SOURCE_EXTENSION = os.path.splitext(os.path.basename(SOURCE))

    apply_transformations(destination_path=DESTPATH,
                          source_basename=SOURCE_BASENAME,
                          source_extension=SOURCE_EXTENSION,
                          source_directory=SOURCE,
                          overlay=OVERLAY)

    NUMBER_OF_FILES_READ_AND_TRANSFORMED += 1

elif SOURCE_TYPE == 'a directory':
    # it's a directory : let's read and transform every file in it.

    for filename in os.listdir(SOURCE):

        # e.g. if SOURCE = img/subdir/ and if filename = file001.jpg
        #           then SOURCE_BASENAME = file001
        #           then SOURCE_EXTENSION = .jpg
        SOURCE_BASENAME, SOURCE_EXTENSION = \
                            os.path.splitext(os.path.basename(os.path.join(SOURCE, filename)))

        apply_transformations(destination_path=DESTPATH,
                              source_basename=SOURCE_BASENAME,
                              source_extension=SOURCE_EXTENSION,
                              source_directory=os.path.join(SOURCE, filename),
                              overlay=OVERLAY)

        NUMBER_OF_FILES_READ_AND_TRANSFORMED += 1

else:
    # SOURCE_TYPE == 'neither a file nor a directory', hopefully something with wildcards.

    SOURCE_DIRECTORY = os.path.dirname(SOURCE)
    SOURCE_NAME = os.path.basename(SOURCE)

    for filename in os.listdir(SOURCE_DIRECTORY):
        if fnmatch.fnmatch(filename, SOURCE_NAME):

            SOURCE_BASENAME, SOURCE_EXTENSION = os.path.splitext(filename)
            # e.g. if SOURCE = img/subdir/ and if filename = file001.jpg
            #           then SOURCE_BASENAME = file001
            #           then SOURCE_EXTENSION = .jpg
            SOURCE_BASENAME, SOURCE_EXTENSION = \
                      os.path.splitext(os.path.basename(os.path.join(SOURCE, filename)))

            apply_transformations(destination_path=DESTPATH,
                                  source_basename=SOURCE_BASENAME,
                                  source_extension=SOURCE_EXTENSION,
                                  source_directory=os.path.join(SOURCE_DIRECTORY, filename),
                                  overlay=OVERLAY)

            NUMBER_OF_FILES_READ_AND_TRANSFORMED += 1

#///////////////////////////////////////////////////////////////////////////////
#
# (2) before quitting
#
#///////////////////////////////////////////////////////////////////////////////

# (2a) removing the embed file used by steghide :
system("rm {0}".format(STEGHIDE__EMBED_FILE))

# (2b) goodbye :
if not ARGS.quiet:
    print("{0} done with \"{1}\" : " \
          "{2} file(s) read and transformed.".format(PROMPT,
                                                     SOURCE,
                                                     NUMBER_OF_FILES_READ_AND_TRANSFORMED))

#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
#///                                                                         ///
#///                          MAIN EXIT POINT                                ///
#///                                                                         ///
#///////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////
