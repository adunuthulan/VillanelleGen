# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

from eda import *
import os

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
ap.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha_sr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_ri", required=False, type=float, help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_rs", required=False, type=float, help="percent of words in each sentence to be swapped")
ap.add_argument("--alpha_rd", required=False, type=float, help="percent of words in each sentence to be deleted")
args = ap.parse_args()

#the output file
from os.path import dirname, basename, join
output = None
if args.output:
    output = join(args.output)
else:
    output = join(dirname(args.input), basename(args.input))

#number of augmented sentences to generate per original sentence
num_aug = 9 #default
if args.num_aug:
    num_aug = args.num_aug

#how much to replace each word by synonyms
alpha_sr = 0.1#default
if args.alpha_sr is not None:
    alpha_sr = args.alpha_sr

#how much to insert new words that are synonyms
alpha_ri = 0.1#default
if args.alpha_ri is not None:
    alpha_ri = args.alpha_ri

#how much to swap words
alpha_rs = 0.1#default
if args.alpha_rs is not None:
    alpha_rs = args.alpha_rs

#how much to delete words
alpha_rd = 0.1#default
if args.alpha_rd is not None:
    alpha_rd = args.alpha_rd

if alpha_sr == alpha_ri == alpha_rs == alpha_rd == 0:
     ap.error('At least one alpha should be greater than zero')

# generate more data with standard augmentation\
# UPDATED for Villanelle Generation
def gen_eda(train_orig, output_file, alpha_sr, alpha_ri, alpha_rs, alpha_rd, num_aug=9):

    lines = open(train_orig, 'r').readlines()

    aug_poems = [[] for _ in range(num_aug)]
    for i, line in enumerate(lines):
        aug_sentences = eda(line, alpha_sr=alpha_sr, alpha_ri=alpha_ri, alpha_rs=alpha_rs, p_rd=alpha_rd, num_aug=num_aug)

        for p in range(num_aug):
            aug_poems[p].append(aug_sentences[p])

    for p in range(num_aug):
        fn = os.path.splitext(output_file)[0] + '_EDA_' + str(p) + os.path.splitext(output_file)[1]
        writer = open(fn, 'w')
        for i, line in enumerate(aug_poems[p]):
            if i in {0, 5, 11, 17}:
                writer.write(aug_poems[p][0] + '\n')
            elif i in {2, 8, 14, 18}:
                writer.write(aug_poems[p][2] + '\n')
            else:
                writer.write(line + '\n')
        writer.close()
        
    print("generated augmented sentences with eda for " + train_orig + " with num_aug=" + str(num_aug))

#main function
if __name__ == "__main__":

    #generate augmented sentences and output into a new file
    gen_eda(args.input, output, alpha_sr=alpha_sr, alpha_ri=alpha_ri, alpha_rs=alpha_rs, alpha_rd=alpha_rd, num_aug=num_aug)