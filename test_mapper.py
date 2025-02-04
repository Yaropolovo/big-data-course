#!/usr/bin/env python3
import sys
import re

REQUIRED_YEARS = [2008, 2010, 2016]

TEST = [
  """<row Id="4" PostTypeId="1" AcceptedAnswerId="7" CreationDate="2008-07-31T21:42:52.667" Score="441" ViewCount="29333" Body="&lt;p&gt;I want to use a track-bar to change a form's opaci
ty.&lt;/p&gt;&#xA;&#xA;&lt;p&gt;This is my code:&lt;/p&gt;&#xA;&#xA;&lt;pre&gt;&lt;code&gt;decimal trans = trackBar1.Value / 5000;&#xA;this.Opacity = trans;&#xA;&lt;/code&gt;&lt;/pre&g
t;&#xA;&#xA;&lt;p&gt;When I try to build it, I get this error:&lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;Cannot implicitly convert type 'decimal' to 'double'.&lt;/p&gt;&#xA;
&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;I tried making &lt;code&gt;trans&lt;/code&gt; a &lt;code&gt;double&lt;/code&gt;, but then the control doesn't work. This code has worked fine for 
me in VB.NET in the past. &lt;/p&gt;&#xA;" OwnerUserId="8" LastEditorUserId="5455605" LastEditorDisplayName="Rich B" LastEditDate="2015-12-23T21:34:28.557" LastActivityDate="2016-07-17
T20:33:18.217" Title="When setting a form's opacity should I use a decimal or double?" Tags="&lt;c#&gt;&lt;winforms&gt;&lt;type-conversion&gt;&lt;decimal&gt;&lt;opacity&gt;" AnswerCoun
t="13" CommentCount="3" FavoriteCount="36" CommunityOwnedDate="2012-10-31T16:42:47.213" />\n
"""]

for line in TEST:
    date_re = re.search('CreationDate=', line)
    if date_re:
        year = int(line[date_re.end()+1:date_re.end()+5])
        if year in REQUIRED_YEARS:
            tags_re = re.search('Tags=', line)
            if tags_re:
                tags = line[tags_re.end():].split('"', maxsplit=2)[1]
                for tag in tags.split('&lt;'):
                    if tag:
                        print(year, tag[:-4], 1, sep='\t')
