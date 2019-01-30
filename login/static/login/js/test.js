var editClass = function(item,text,func,index_i = -1,expect_i = -1)
{
    item.forEach(function(item,index)
    {
	if(index_i == -1)
	{
	    if(index != expect_i)
	    {
		func(item,text);
	    }
	}
	else
	{
	    if(index == index_i)
		func(item,text);
	}
	
    });
}

var addClass = function(item,text)
{
    item.classList.add(text);
}

var removeClass = function(item,text)
{
    item.classList.remove(text);
}

var ifRemoveClass = function(item,text)
{
    if(item.classList.contains(text)) item.classList.remove(text);
    else item.classList.add(text);
}

var formSystem = function()
{
    var tab_item = document.querySelectorAll('.form-button');
    var tab_content = document.querySelectorAll('.form-content');    

    var text = "hidden-item";

    tab_item.forEach(function(item,index)
    {
	item.addEventListener('click', function() {
	    editClass(tab_content,text,addClass,-1,index);
	    editClass(tab_content,text,ifRemoveClass,index);
	});
    });

}

var switchSystem = function()
{
/*
コンテンツを前取得し、全て非表示にする
押下されたタブ要素を取得し、それに応じたindexのコンテンツを表示する。

*/
    var tab_item = document.querySelectorAll('.tab_item');
    var tab_content = document.querySelectorAll('.tab_content');

    var text = "hidden-item";

    tab_item.forEach(function(item,index)
    {
	item.addEventListener('click', function() {
	    editClass(tab_content,text,addClass);
	    editClass(tab_content,text,removeClass,index);
	    
	});
    });
}

window.onload = function()
{
    switchSystem();
    formSystem();

}
