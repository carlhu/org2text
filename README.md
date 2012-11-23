Let's say I have created following outline in Emacs's Orgmode:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
My Todo List
* At work
     * Call John :URGENT:
     * Optimize the logging system :MEDIUM:
           * Eliminate callout and process switch 
             so that context switch costs and cache 
             coherency is improved.
* At home
     * Buy supplies :OPTIONAL:
           * Address
             Pearl Paint
             111 8th Avenue
             New York City
           * Pencil
           * Eraser
     * Clean up apartment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I find this presentation of my thoughts clear and simple: Orgmode's decisions seem to me to be optimal. Mr. Dominik is a marvelously talented engineer and designer. Now, if I want to send a collegague the outline, I can simply send him the text file. Unfortunately, the raw text file for this outline is:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
My Todo List
* At work
** Call John :URGENT:
** Optimize the logging system :MEDIUM
*** Eliminate callout and process switch 
so that context switch costs and cache 
coherency is improved.
* At home
** Buy supplies :OPTIONAL:
*** Address
Pearl Paint
111 8th Avenue
New York City
** Pencil
** Eraser
* Clean up apartment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although I am happy that the Orgmode uses a plain text file, reading this in a non-Emacs editor is an uninviting experience. 'Drawers' (i.e. 'Pearl Paint...') are not properly aligned with the heading (i.e. 'Address'). No indentation is used. Long lines that wrap do not stay aligned. Since I often need to share my thoughts with non-Emacs users, I designed a solution optimized for my own needs, Org2Text. Org2Text implements the following requirements:

1. *Use plain text*. It's easy to present beautiful outlines in HTML, but I often need to use plain text email as well as save in README files that are meant to be read directly in text editors. So, the exported outline must be elegant to read with only a text editor or `cat` on a Unix command line.
1. *Clean alignment*. 4 spaces for every additional star. Drawers are properly aligned. Long lines are wrapped and indented correctly.
1. *Bullets can use unicode for clarity.** Through experimentation, everyone I need to work with now uses editors and email that supports Unicode. Use the following three increasingly small bullets: `●`, `•`, and `∙`.
1. *Drawers are indicated with `|`*. Drawers can be quite lengthy: I often put the idea in the heading, and write out the prose in the drawer, so I need a clear indication regarding which heading drawer text refers to. `|` is the tradition email blockquotes now use, and Org2Text also uses this.
1. *Tags*. Tags at the end of headings is hard to parse since they are not vertically aligned. Put them in the front and surround them with the latin quote characters: `‹URGENT›`. 

The following is a transform of the above outline satisfying these five requirements:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 At work 
     • ‹URGENT› Call John 
     • ‹IMPORTANT› Optimize the logging system 
          ∙ Eliminate callout and process switch 
● At home 
     • ‹OPTIONAL› Buy supplies 
          ∙ Address 
            | Pearl Paint 
            | 111 8th Avenue 
            | New York City 
     • Pencil 
     • Eraser 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
