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
        $ watersteg.py --inputfile IMG_4280.JPG --passphrase="secret phrase" --message="Hello !"
  ______________________________________________________________________________

  transformations :

        (1) the original image is resized, watermarked and steghide'd.

                (resize 400x... + watermark + steghide)

                The watermark is a text added at several places on the
                image.

                new file name : FILENAME__TRANS1

        (1) the original image is steghide'd.

                new file name : FILENAME__TRANS2
  ______________________________________________________________________________

  arguments :

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
  ______________________________________________________________________________

  history :

        o version 1 (2015_08_25)

                initial version, pylint:10
"""

import argparse
import os.path
import sys

PROGRAM_VERSION = "1"
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

    # TEST : does "convert" exist ?
    if result and system("convert -version > tmpfile_zzz") != 0:
        print("... ImageMagic/convert can't be find : the program has to stop.")
        result = False

    # TEST : does "steghide" exist ?
    if result and system("steghide --version > tmpfile_zzz") != 0:
        print("... steghide can't be find : the program has to stop.")
        result = False
    system("rm tmpfile_zzz")

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

    parser.add_argument('--inputfile',
                        type=str,
                        required=True,
                        help="input file")

    parser.add_argument('--outputpath',
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
#///                            ENTRY POINT                                  ///
#///////////////////////////////////////////////////////////////////////////////

#///////////////////////////////////////////////////////////////////////////////
# (0) warm-up //////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

# (0.a) arguments from the command line
ARGS = get_args()
QUIET = (ARGS.quiet == 'True')
DEBUG = (ARGS.debug == 'True')

# (0.b) input file, output path
INPUTFILE = ARGS.inputfile
BASENAME, EXTENSION = os.path.splitext(os.path.basename(INPUTFILE))

OUTPUTPATH = ARGS.outputpath
if not OUTPUTPATH.endswith("/"):
    OUTPUTPATH += "/"

# (0.c) summary
if not QUIET:
    print("=== {0} v. {1} === ".format(PROGRAM_NAME,
                                       PROGRAM_VERSION))
    print("... input file=\"{0}\"".format(INPUTFILE))
    print("... output path=\"{0}\"".format(OUTPUTPATH))

# (0.d) are the required external programs available ?
if not external_programs_are_available():
    sys.exit()

# (0.e) creating the embed file used by steghide :
with open(STEGHIDE__EMBED_FILE, "w") as steghide_message:
    steghide_message.write(ARGS.message)

#///////////////////////////////////////////////////////////////////////////////
# (1) first transformation /////////////////////////////////////////////////////
#       resize 400 + watermark + steghide
#///////////////////////////////////////////////////////////////////////////////

# (temp file, to be deleted) :
TMPFILENAME = "{0}{1}_400x{2}".format(OUTPUTPATH, BASENAME, EXTENSION)
system("convert \"{0}\" -resize 400 \"{1}\"".format(INPUTFILE, TMPFILENAME))

FILENAME__TRANS1 = "{0}{1}_400x_watermark_steghide{2}".format(OUTPUTPATH, BASENAME, EXTENSION)
system("convert -size 240x160 xc:none -fill grey " \
       "-gravity NorthWest -draw \"text 10,10 '{2}'\" " \
       "-gravity SouthEast -draw \"text 5,15 '{2}'\" miff:- " \
       "| composite -tile - \"{0}\" \"{1}\"".format(TMPFILENAME,
                                                    FILENAME__TRANS1,
                                                    ARGS.message))

system("steghide embed -cf \"{0}\" -ef \"{1}\" -p \"{2}\" -q".format(FILENAME__TRANS1,
                                                                     STEGHIDE__EMBED_FILE,
                                                                     ARGS.passphrase))

system("rm {0}".format(TMPFILENAME))

#///////////////////////////////////////////////////////////////////////////////
# (2) second transformation ////////////////////////////////////////////////////
#       steghide
#///////////////////////////////////////////////////////////////////////////////

FILENAME__TRANS2 = "{0}{1}_steghide{2}".format(OUTPUTPATH, BASENAME, EXTENSION)

system("steghide embed -cf \"{0}\" -ef \"{1}\" " \
       "-p \"{2}\" -q -sf \"{3}\" -f".format(INPUTFILE,
                                             STEGHIDE__EMBED_FILE,
                                             ARGS.passphrase,
                                             FILENAME__TRANS2))

#///////////////////////////////////////////////////////////////////////////////
# (3) before quitting //////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////

# (3a) removing the embed file used by steghide :
system("rm {0}".format(STEGHIDE__EMBED_FILE))

# (3b) goodbye :
if not QUIET:
    print("... done with \"{0}\"".format(INPUTFILE))
