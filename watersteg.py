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
    ❏Watersteg project❏

     waterhide.py : apply a watermark & steghide

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

        NB : the destination path must exist.
  ______________________________________________________________________________

  transformations :

        (1) the original image is resized, watermarked and steghide'd.

                o function transform1__r400_wm_s()
                o (resize 400x... + watermark + steghide)
                o the watermark is a text added at several places on the
                  image.
                o new file name : FILENAME__TRANS1

        (2) the original image is steghide'd.

                o function transform2__steghide()
                o new file name : FILENAME__TRANS2
  ______________________________________________________________________________

  arguments :

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
  ______________________________________________________________________________

  history :

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
  ______________________________________________________________________________

    return value/error messages

        o no error value is returned.
        o error messages begin with "... !!", normal messages with "..." .
        o the --quiet option turns off normal messages, not the error ones.
          the --debug option turns on debug messages and has no effect on the normal
          or the error ones.
"""

import argparse
import os.path
import sys
import tempfile

PROGRAM_VERSION = "2"
PROGRAM_NAME = "Watersteg"

# file where the message to be embed will be written. This file will be erased
# (see the end of the file).
STEGHIDE__EMBED_FILE = "steghide.embed"

#///////////////////////////////////////////////////////////////////////////////
def system(order):
    """
        Give a system "order" through a call to os.system() .

        Display the order if an error occurs and stop the program.
    """
    if DEBUG:
        print("@@ os.system() : \"{0}\"".format(order))

    return os.system(order) #subprocess.call(order, shell=True)

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
            print("... !! ImageMagic/convert can't be find : the program has to stop.")
            result = False

        # TEST : does "steghide" exist ?
        if result and system("steghide --version > {0}".format(tmpfile.name)) != 0:
            print("... !! steghide can't be find : the program has to stop.")
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
                        help="input file")

    parser.add_argument('--destpath',
                        type=str,
                        default=".",
                        help="output path")

    parser.add_argument('--debug',
                        type=str,
                        choices=('True', 'False'),
                        default="False",
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
                        type=str,
                        choices=('True', 'False'),
                        default="False",
                        help="disallow common messages' display; " \
                             "only the error messages will be display")

    return parser.parse_args()

#///////////////////////////////////////////////////////////////////////////////
def transform1__r400_wm_s(sourcefilename, destfilename):
    """
        transformation :

                source file -> source file + resize 400 + watermark + steghide
    """
    with tempfile.NamedTemporaryFile(mode='w', delete='True') as tmpfile:

        # resize 400x...
        system("convert \"{0}\" -resize 400 \"{1}\"".format(sourcefilename,
                                                            tmpfile.name))

        if not QUIET:
            print("... creating {0} ....".format(destfilename))

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
    """
    if not QUIET:
        print("... creating {0} ....".format(destfilename))

        system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
               "-p \"{2}\" -q -sf \"{3}\" -f".format(sourcefilename,
                                                     STEGHIDE__EMBED_FILE,
                                                     ARGS.passphrase,
                                                     destfilename))

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
QUIET = (ARGS.quiet == 'True')
DEBUG = (ARGS.debug == 'True')

# (0.b) input file, output path
SOURCE = ARGS.source
BASENAME, EXTENSION = os.path.splitext(os.path.basename(SOURCE))

DESTPATH = ARGS.destpath
if not DESTPATH.endswith("/"):
    DESTPATH += "/"
if not os.path.exists(DESTPATH):
    print("... !! the destination path \"{0}\"doesn't exist : " \
          "the program has to stop.".format(DESTPATH))
    sys.exit()

# (0.c) files to be created
FILENAME__TRANS1 = "{0}{1}_400x_watermark_steghide{2}".format(DESTPATH, BASENAME, EXTENSION)
FILENAME__TRANS2 = "{0}{1}_steghide{2}".format(DESTPATH, BASENAME, EXTENSION)

# (0.d) displaying summary
if not QUIET:
    print("=== {0} v. {1} === ".format(PROGRAM_NAME,
                                       PROGRAM_VERSION))
    print("... input file=\"{0}\"".format(SOURCE))
    print("... output path=\"{0}\"".format(DESTPATH))

# (0.e) are the required external programs available ?
if not external_programs_are_available():
    sys.exit()

# (0.f) creating the embed file used by steghide :
with open(STEGHIDE__EMBED_FILE, "w") as steghide_message:
    steghide_message.write(ARGS.message)

#///////////////////////////////////////////////////////////////////////////////
#
# (1) transformations
#
#///////////////////////////////////////////////////////////////////////////////

transform1__r400_wm_s(SOURCE, FILENAME__TRANS1)
transform2__steghide(SOURCE, FILENAME__TRANS2)

#///////////////////////////////////////////////////////////////////////////////
#
# (2) before quitting
#
#///////////////////////////////////////////////////////////////////////////////

# (2a) removing the embed file used by steghide :
system("rm {0}".format(STEGHIDE__EMBED_FILE))

# (2b) goodbye :
if not QUIET:
    print("... done with \"{0}\"".format(SOURCE))
