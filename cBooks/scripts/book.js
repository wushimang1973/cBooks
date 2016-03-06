

var BaseScript="/cBooks/scripts/book.py?RequestType=";
var HTMLbegin = '<html><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="/cBooks/html/chinese.css"></head><body>';
var HTMLend = '</body></html>';

var IS_IOS = IsIOS();

var CommentField = '<span class="comment_field"><input type="text" size="40" id="comment_content" value=""/><button type="button" id="add_button_field">search</button></span>';
var iPadComment;

function AddComment(e)
{
    clearTimeout(iPadComment);
    var BookName    = Base64.encode($("#book_name option:selected").text());
    var ChapterName = Base64.encode($("#book_chapter option:selected").text());
    var Selected = window.getSelection();
    var ParentText = Selected.anchorNode.textContent;
    var BijiBlock = $("div.biji_block:contains('"+ParentText+"')").find(".biji_head").clone();
    if (BijiBlock.text() == "")
    {
	return;
    }
    //BijiBlock.find("span").remove();
    var BijiTitle = BijiBlock.html();
    var SelectedText = ParentText.substring(Selected.anchorOffset-10,Selected.anchorOffset);
    
    if (IS_IOS)
    {
	SelectedText += ParentText.substring(Selected.extentOffset+1,Selected.extentOffset); // in iOS context, usually will want to add comments after a stop mark which is often to the immediate right of the selection 	
    }
    if (SelectedText.length > 0 && ParentText.length > 0)
    {
	var Comment='';
	if (! IS_IOS)
	{
	    Comment=prompt("Insert a comment after "+SelectedText);	    
	    if (Comment.length == 0)
	    {
		return
	    }
	    Comment=Base64.encode(Comment);
	    BijiTitle=Base64.encode(BijiTitle);
	    SelectedText=Base64.encode(SelectedText);
	    var FinalURI = BaseScript+"AddComment&BookName="+BookName+"&ChapterName="+ChapterName+"&BlockName="+BijiTitle+"&SelectedText="+SelectedText+"&CommentText="+Comment;
	    $.getJSON(FinalURI);
	}
	else
	{
	    iPadComment = setTimeout(function(){
		Comment=prompt("Insert a comment after "+SelectedText);	    
		if (Comment.length == 0)
		{
		    return;
		}
		Comment=Base64.encode(Comment);
		BijiTitle=Base64.encode(BijiTitle);
		SelectedText=Base64.encode(SelectedText);
		var FinalURI = BaseScript+"AddComment&BookName="+BookName+"&ChapterName="+ChapterName+"&BlockName="+BijiTitle+"&SelectedText="+SelectedText+"&CommentText="+Comment;
		$.getJSON(FinalURI);		
	    },5000);
	}
    }
}
function ToggleCommentary()
{
    if ($(".zhipi").css('display') == 'inline')
    {
	$(".zhipi").css('display','none');
    }
    else
    {
	$(".zhipi").css('display','inline');
    }
}
function SearchContent()
{
    
    var BookName    = Base64.encode($("#book_name option:selected").text());
    var ChapterName = Base64.encode($("#book_chapter option:selected").text());
    var SearchContents = Base64.encode($("#search_content").val());
    $("#baiwen").attr('checked',false);

    if (BookName == "" )
    {
	BookName = "Kg==";    // b64-encoded "*" to signify wildcarding
    }
    if (ChapterName == "")
    {
	ChapterName = "Kg==";
    }
    var FinalURI = BaseScript+"SearchContent&BookName="+BookName+"&ChapterName="+ChapterName+"&SearchContents="+SearchContents+"&SearchRange="+Base64.encode($("#search_range").val());
    $.getJSON(FinalURI,function(data)
	      {
		  Dbg(data);
		  var buf = '';
		  for (var i = 0; i < data.results.length; i++)
		  {
		      var Source = Base64.decode(data.results[i].source);
		      var Contents = Base64.decode(data.results[i].contents);
		      if (Contents.search("biji_head") == -1 ) // no biji "head" if you're dealing with a paragraph from a novel.  So use the source as the "head"
		      {
			  Contents = '<div class="biji_head">'+Source+'</div>'+Contents;
		      }
		      else
		      {
			  Contents = Contents.replace(/<div class="biji_head">(.*?)<\/div>/,'<div class="biji_head"><span class="source_note">'+Source+"<br></span>$1"+"</div>")
			  
		      }
		      buf += Contents;
		  }
		  $("#mainContent").html(HTMLbegin+buf+HTMLend);
	      }
	     );
    return;
}

function ShowSearchButton()
{
    Reveal($("#search_button"));
    Reveal($("#search_zhipi_field"));
}

function GetChapterContent(e)
{
    var Chapter = Base64.encode(e.currentTarget.value);
    var Book = Base64.encode($("#book_name option:selected").text());
    var FinalURI = BaseScript+"GetChapter&BookName="+Book+"&ChapterName="+Chapter;
    $.getJSON(FinalURI,function(data)
	      {
		  $("#mainContent").html(Base64.decode(data.chapter_contents));
		  var FirstEntry = $(".biji_block")[0];
		  FirstEntry.innerHTML=CommentField+FirstEntry.innerHTML;
		  if (IS_IOS)
		  {
		      $(".biji_entry").css("font-size","18pt");
		      $(".biji_head").css("font-size","20pt");
		      
		  }
	      }
	     );
    $("#baiwen").attr('checked',false);

}

function GetBookChapters(e)
{
    var Selection=Base64.encode(e.currentTarget.value);
    var FinalURI = BaseScript+"ListChapters&BookName="+Selection;
    $.getJSON(FinalURI,function(data)
	      {
		  var ChapterBuf = $("#book_chapter");
		  var NameBuf = '<option value=""></option>\n';
		  for (var i = 0; i < data.chapterlist.length; i++)
		  {
		      
		      NameBuf += '<option value="'+data.chapterlist[i]+'">'+data.chapterlist[i]+'</option>\n';		      
		  }
		  $("#book_chapter").html(NameBuf);
	      }
	     );
    $("#baiwen").attr('checked',false);

    
}


function FirstTime()
{
    $.getJSON(BaseScript+"ListBooks",function(data)
	      {
//		  Dbg(data);
		  var NameBuf=$("#book_name").html();
		  for (var i = 0; i < data.booklist.length; i++)
		  {
		      NameBuf += '<option value="'+data.booklist[i]+'">'+data.booklist[i]+'</option>\n';
		  }
		  $("#book_name").html(NameBuf);
	      }
	     );
    $("#book_name").change(GetBookChapters);
    $("#book_chapter").change(GetChapterContent);
    $("#search_content").change(ShowSearchButton);
    $("#search_button").click(SearchContent);
    $("#baiwen").click(ToggleCommentary);
    $("#add_comment").click(AddComment);

    if (IS_IOS)
    {
	$(".console").css('top','10pt');
    }
    else
    {
	$("#add_comment").css("display","inline");

    }
}

$(document).ready(FirstTime);
if (IS_IOS)
{
    document.addEventListener("selectionchange",AddComment);
    
}
