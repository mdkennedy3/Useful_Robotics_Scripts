#Written by Tarik Tuson & Monroe Kennedy

from pyPdf import PdfFileReader, PdfFileWriter
from pyPdf.pdf import PageObject

import sys, getopt, os, ast


class Generate_Scaled_Apriltags(object):
    """docstring for Generate_Scaled_Apriltags"""
    def __init__(self, input_file_name, output_file_name, orig_tag_side_length, desired_tag_side_length, margin_factor, tag_numbers):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.orig_tag_side_length = orig_tag_side_length
        self.desired_tag_side_length = desired_tag_side_length
        self.margin_factor =margin_factor
        self.tag_numbers = tag_numbers

    def gen_april_tag(self):
        orig_tag_side_length =self.orig_tag_side_length  # mm
        desired_tag_side_length = self.desired_tag_side_length #mm
        margin_factor = self.margin_factor # page margin (as percentage)
        scale_factor = desired_tag_side_length / orig_tag_side_length
        tags_per_row = int(1*(1-2*margin_factor)/scale_factor)
        tags_per_col = tags_per_row #they're the same.
        #
        tag_numbers = self.tag_numbers 
        # fname is the tag source file:
        fname = self.input_file_name #'/home/tarik/catkin_ws/src/apriltags_ros/apriltags/tags/tag36h11.pdf'
        outname = self.output_file_name #'/home/tarik/pyAprilScale/test.pdf'
        with open(fname, 'rb') as inf, open(outname, 'wb') as ouf:
            inpdf = PdfFileReader(inf) 
            outpdf = PdfFileWriter()
            print "tag number", tag_numbers
            inPages = [inpdf.getPage(t) for t in tag_numbers]
            (w,h) = inPages[0].mediaBox.upperRight
            o = PageObject.createBlankPage(outpdf, w,h) 
            # begin adding pages to the output pdf:
            rowIdx = 0
            colIdx = 0
            for p in inPages:
                print "scalef", type(scale_factor), "rowidx", type(float(rowIdx)), "margin_factor", type(margin_factor), "w", type(w), "h", type(h)
                o.mergeScaledTranslatedPage(p, scale_factor,
                                        (scale_factor*float(rowIdx) + margin_factor)*float(w),
                                        (scale_factor*colIdx + margin_factor)*float(h) )
                rowIdx+=1
                if rowIdx == tags_per_row:
                    colIdx+=1
                    rowIdx = 0 
                if colIdx == tags_per_col:
                    outpdf.addPage(o)
                    o = PageObject.createBlankPage(outpdf, w,h)
                    colIdx = 0
            outpdf.addPage(o)
            outpdf.write(ouf)


def main(argv):
    print "obtaining file"
    try: 
        opts, args = getopt.getopt(argv, "hf:o:t:lo:lf",["file_name=","ouput_name=","tag_numbers=","original_length=", "final_length="])
    except getopt.GetoptError:
        print "pyAprilScale.py -f /full/path/to/file  -o file_output_name --t='[0,1,2]' -lo orig_length_mm  -lf des_length_mm "


    out_dir = []
    file_input = []

    tag_numbers = range(0,10) #defualt
    cwd = os.getcwd() #get current working directory
    orig_tag_side_length = 173.0 # mm
    desired_tag_side_length= 20.0 #mm

    for opt, arg in opts:
        if opt == '-h':
            print "pyAprilScale.py -f /full/path/to/file  -o file_output_name"
            sys.exit()
        elif opt in ["-f","--file_name"]:
            file_input = arg
        elif opt in ["-o","--ouput_name"]:
            out_dir = cwd+'/' + arg
        elif opt in ["-t", "--tag_numbers"]:
            tag_numbers = ast.literal_eval(arg)
        elif opt in ["-lo","original_length"]:
            orig_tag_side_length = float(arg)
        elif opt in ["-lf","final_length"]:
            desired_tag_side_length = float(arg)



    margin_factor = 0.05 # page margin (as percentage)
    


    cls_obj = Generate_Scaled_Apriltags(file_input, out_dir, orig_tag_side_length, desired_tag_side_length, margin_factor, tag_numbers)
    cls_obj.gen_april_tag()

if __name__ == '__main__':
    main(sys.argv[1:])


