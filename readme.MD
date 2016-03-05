MOTIVATION

This is an edition of the great classical text 《欽定詞譜》 formatted into HTML that is amenable to browsing (using "book.html" and "chinese.css") and searching (using "book.py" and "book.js").  The format used for both browsing and searching is generalized and can be (has been) applied for the storage and analysis of other Classical texts.  It is hoped that dissemination of both texts and support scripts via GitHub provides both modern, convenient access to the great scholarship of the past and a way for people to provide corrections to digital forms of these texts, which are often present on sites such as ctext.org along with terrible typos due to OCR and entry mistakes.  Perhaps if people are interested, they can use GitHub versioning system to provide corrections for everyone as they come across them.  If there is sufficient interest I'd be happy to upload additional texts formatted for these types of actions.  Currently the list is:

子不語
彈指詞
碧巖錄
紅樓夢
花間集
昭明文選
欽定詞譜
淥水亭識
通志堂集
隨園詩話
養拙異聞
納蘭詞全集
清代閨秀詩話

SETUP

As the interface to the books is web based, the system requires a working web browser installation.  Python 3 is required for the scripts and jQuery >= 1.9.1 is required for javascript.  The scripts are crude but perform reasonably well.  Any thoughts or constructive comments are welcome to leave here.  


1) the files assume the following structure relative to your webroot /:

	/cBooks/books/<bookName>/*.html
	/cBooks/scripts/<JS,PY>
	/cBooks/html/<HTML,CSS>

and this is what will populate with git clone.  The only manual action should be done in book.html, where you need to adjust "/path/to/jquery-1.9.1.min.js" to point to wherever your jquery lives.

if using HTTPS, I have had occasional DOM-related issues.  You may need to adjust "var SecureDomain" in "scripts/common.js" accordingly

2) the scripts assume that your python 3 lives at "/usr/bin/python3"

