# -*- coding: utf-8 -*-
#
# Org2Text
#
# Authored by Carl Hu 2012
# Copyright 2012 Carl Hu
# 
# This program is distributed under the terms of the GNU General Public License.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.

import sys
import os
import re

SPACES_PER_INDENT_LEVEL = 5

TABLE_MARKER = '!#TABLE#!'
def table_clean(line):
    ''' Line up tables to the indent. Make the corners nice. '''
    l = line.lstrip()
    if len(l)>0 and l[0]=='|':
        return TABLE_MARKER + line.replace('|', ' ').replace('+', '-').replace('-',u'\u2015')[1:]
    else:
        return line

def extract_tags(line):
    sections = line.split(' :')
    if len(sections) > 1:
        tags = [tag for tag in sections[1].split(':') if tag]
        return u'\u2039%s\u203a %s' % (','.join(tags), sections[0])
    else:
        return line

BULLETS = { 1: u'\u25cf',  # Bigger black circle
            2: u'\u2022',  # Medium circle (bullet)
            3: u'\u2219' } # Dot

whitespace_matcher = re.compile(u'^[\s%s]*' % ''.join(BULLETS.values())) 
def count_leading_spaces(inp):
    ret = whitespace_matcher.search(inp)
    if ret: return len(ret.group())
    else: return 0

def get_indent(indent, line, is_drawer):
    if len(line.strip()) == 0: 
        return (indent, line, is_drawer)
    for i in range(10, 0, -1):
        if line.startswith('*' * i + ' '):
            c = BULLETS.get(i, u'\u2219')
            base_line = extract_tags(line[i:].lstrip())
            return (i, c + ' ' + base_line, False)
    # it's a drawer if it has no * on it.
    base_line = extract_tags(line)
    return (indent, table_clean(base_line), True)

def canonicalize_word(word):
    if len(word.strip()) == 0: return word # keep the spaces
    if word[-1]==' ': return word
    else: return word + ' '

def render(block, width, hang, do_quote):
    lines = []
    quote_prefix, len_quote_prefix = (u'| ', 2) if do_quote else  ('', 0)
    hang = hang + len_quote_prefix
    leader = count_leading_spaces(block)
    if block.startswith(TABLE_MARKER): 
        return ' '*(hang + leader) + quote_prefix + block[len(TABLE_MARKER):] 
    for paragraph in block.split('\n'):
        line = ''
        tokenlist = [' '*hang + quote_prefix + ' '*(leader if do_quote else 0)] + paragraph.split()
        for word in tokenlist: # word wrap.
            word = canonicalize_word(word)
            if len(line) + len(word) < width:
                line = line + word            
            else:
                # print 'LEADER', leader, 'HANG', hang, "PREFIXLEN:", ('APPEND/B:[%s]' % line).encode('utf-8')
                lines.append(line)
                curr_quote_prefix = quote_prefix if do_quote else '  ' # headings get spaces for wrapped lines.
                line = ' '*hang + curr_quote_prefix + ' ' * (leader if do_quote else 0) + word
        # print 'LEADER', leader, 'HANG', hang, "PREFIXLEN:", ('APPEND/B:[%s]' % line).encode('utf-8')
        lines.append(line)
    return '\n'.join(lines)

def convert(input_file, output_file):
    indent_level = 0
    is_drawer = False
    for line in input_file.read().splitlines():
        line = line.decode('utf-8')
        indent_level, line_out, is_drawer = get_indent(indent_level, line, is_drawer)
        hang = SPACES_PER_INDENT_LEVEL * (indent_level - 1)
        output_file.write((render(line_out, 80, hang, is_drawer) + '\n').encode('utf-8'))
        
# Main
f_output = sys.argv[1]
outfile = open('/home/carlhu/tmp/' + os.path.basename(f_output).split('.')[0] + '.export.txt', mode='w')
convert(sys.stdin, outfile)
