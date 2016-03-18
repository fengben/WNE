#!/usr/bin/env python
# encoding: utf-8
import argparse


from jinja2 import Environment, FileSystemLoader
import os

# Capture our current directory
BASE_DIR= os.path.dirname(os.path.abspath(__file__))

def template2md(filename):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(BASE_DIR),
                         trim_blocks=True)
    print j2_env.get_template(filename).render(
        title='Hello World'
    )

def create_note(args):
    template = args.template
    template2md(template)
    print("Load template from: {}".format(template))

def main():
    parser = argparse.ArgumentParser(prog="convert") # 设定命令信息，用于输出帮助信息
    parser.add_argument("-t", "--template", required=False, default="template.tpl")
    parser.add_argument("-f") # Accept Jupyter runtime option
    args = parser.parse_args()
    create_note(args)

if __name__ == "__main__":
    main()
