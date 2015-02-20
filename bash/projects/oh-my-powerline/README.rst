===============
Oh My Powerline
===============

About
=====
A zsh-native minimal implementation of `Powerline <https://github.com/Lokaltog/powerline>`_ for use with oh-my-zsh & antigen.

Several existing prompts/themes were very helpful when working on this:

- `agnoster                     <https://gist.github.com/agnoster/3712874>`_
- `oh my zsh powerline theme    <https://github.com/jeremyFreeAgent/oh-my-zsh-powerline-theme>`_
- `powerline                    <https://github.com/Lokaltog/powerline>`_
- `pure                         <https://github.com/sindresorhus/pure>`_
- `seeker                       <https://github.com/tonyseek/oh-my-zsh-seeker-theme>`_
- `steve losh                   <http://stevelosh.com/blog/2010/02/my-extravagant-zsh-prompt/>`_
- `wedisagree                   <https://github.com/robbyrussell/oh-my-zsh/blob/master/themes/wedisagree.zsh-theme>`_



Preview
=======
Sample screenshot:

.. image:: https://i.imgur.com/TJ8FcRa.png

Installation
============
Oh-My-Zsh:

    wget -P ~/.oh-my-zsh/themes/ https://github.com/nfarrar/oh-my-powerline/blob/master/oh-my-powerline.zsh-theme

Antigen:

    antigen theme nfarrar/oh-my-powerline oh-my-powerline


Symbols
=======
The unicode values for the powerline symbols are::

    # Escape Sequence Binding                               Glyph
    # ----------------------------------------------------- -----
    POWERLINE_SYMBOL_VERSION_CONTROL=$(echo -n '\ue0a0')    # 
    POWERLINE_SYMBOL_LINE=$(echo -n '\ue0a1')               # 
    POWERLINE_SYMBOL_PADLOCK=$(echo -n '\ue0a2')            # 
    POWERLINE_SYMBOL_ARROW_RIGHT_BLACK=$(echo -n '\ue0b0')  # 
    POWERLINE_SYMBOL_ARROW_RIGHT=$(echo -n '\ue0b1')        # 
    POWERLINE_SYMBOL_ARROW_LEFT_BLACK=$(echo -n '\ue0b2')   # 
    POWERLINE_SYMBOL_ARROW_LEFT=$(echo -n '\ue0b3')         # 




