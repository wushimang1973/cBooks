var SecureDomain="https://your.domain/";

function IsIpad()
{
    if (navigator.userAgent.match(/iPad/i))
    {
	return true;
    }
    return false;
}

function IsIphone()
{
    if (navigator.userAgent.match(/iPhone/i))
    {
	return true;
    }
    return false;
}

function IsIOS()
{
    return (IsIpad() || IsIphone());
}


function ToggleDisplay(el)
{
    if ($(el).is(":visible"))
    {
	$(el).css("display","none");
    }
    else
    {
	$(el).css("display","inline");
    }
}

function Reveal(el)
{
    if ($(el).css('display')=='none')
    {
	$(el).css('display','inline');
    }

}
function Dbg(string)
{
    console.log(string);
}


function IsChecked(box)
{
    return box.is(":checked");
}

function jName(type,name)
{
    return type+"[name="+name+"]";
}

function Show(el)
{
    el.css('display','inline');
}

function Hide(el)
{
    el.css('display','none');
}

function DivBlock(id,content,name,type)
{
    var ExtraContent="";

    if (name)
    {
	ExtraContent += ' name="'+name+'"';
    }
    if (!type)
    {
	type = "class";
    }
    return '<div '+type+'='+id+ExtraContent+'>'+content+'</div>';
}

function Pblock(Class,title,link)
{
    return '<p class="'+Class+'entry" id="'+link+'">'+title+'</p>';
}

function Param(name,value)
{
    return "&"+name+"="+value;
}


function EscapeChar(param)
{
   param = param.replace(/#/g,"&#35");
   param = param.replace(/</g,"&lt;");
   param = param.replace(/>/g,"&gt;"); 
   param = param.replace(/\"/g,"&quot;")
   return(param)
}

function ReturnOption(value,content)
{
    return '<option value="'+value+'">'+content+'</option';
}

function ActiveDebug()
{
    LoadRes("common.css");
    $("body").append('<div id="debug_pane"></div>');
}

function LoadRes(RES,Buffer,CallbackFunc)
{
    type = RES.split(".")[(RES.split(".")).length - 1].toLowerCase();
    RES = ReturnDomainContext()+"/.websupport/"+type+"/"+RES;
    if (!Buffer) // add the resource ex CSS/JS to header section
    {
	var fileref = document.createElement("link");    
	fileref.setAttribute("rel","stylesheet");
	fileref.setAttribute("type","text/css");
	fileref.setAttribute("href",RES);
	document.getElementsByTagName("head")[0].appendChild(fileref);	
    }
    else
    {
	$.get(RES,
	    function(data)
	    {
		Buffer.html(data);
		if (CallbackFunc)
		{
		    CallbackFunc(Buffer);
		}
	    }
	);
    }
}

// https://stackoverflow.com/questions/2897155/get-cursor-position-in-characters-within-a-text-input-field
(function($) {
    $.fn.getCursorPosition = function() {
	var input = this.get(0);
        if (!input) return; // No (input) element found
        if ('selectionStart' in input) {
	                // Standard-compliant browsers
            return input.selectionStart;
        } else if (document.selection) {
            // IE
            input.focus();
            var sel = document.selection.createRange();
            var selLen = document.selection.createRange().text.length;
            sel.moveStart('character', -input.value.length);
            return sel.text.length - selLen;
        }
    }
})(jQuery);
