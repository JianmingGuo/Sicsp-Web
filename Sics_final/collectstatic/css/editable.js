function editCell(event){
	var currentCell;

	if(event == null){
		currentCell = window.event.srcElement;
	}else{
		currentCell = event.target;
	}

	if(currentCell.tagName.toLowerCase() == "td"){
		var input = document.createElement("input");
        input.type = 'text';
        input.setAttribute('class', 'editable');
        input.value = currentCell.innerHTML;
        input.width = currentCell.style.width;

        input.onblur = function(){
            currentCell.innerHTML = input.value;
            //currentCell.removeChild(input);
        };
        input.onkeydown = function(event){
            if(event.keyCode == 13){
                input.blur();
            }
        };

        currentCell.innerHTML = '';
        currentCell.appendChild(input);
        input.focus();
	}
}

function insRow(id,num,key,data) {
  var x = document.getElementById(id).insertRow(num);
  var c1 = x.insertCell(0);
  var c2 = x.insertCell(1);
  var c3 = x.insertCell(2);
  var c4 = x.insertCell(3);
  var c5 = x.insertCell(4);
  var c6 = x.insertCell(5);
  c1.innerHTML = key;
  c2.innerHTML = data[key];
  c3.innerHTML = "<input name='NET' type='checkbox' value=''>网络</input><input name='FILE' type='checkbox' value=''>文件</input>";
  c4.innerHTML = c5.innerHTML = c6.innerHTML = "";
}

function update(id) {
    var formdata = new FormData();
    var tableInfo = "";
    var tableObj = document.getElementById(id);
    // var check = $("input[type='checkbox']:checked");//在table中找input下类型为checkbox属性为选中状态的数据
    // var list;
    // check.each(function () {//遍历
    //             var row = $(this).parent("td").parent("tr");
    //             var id = row.find("[name='NET']").html(); //注意html()和val()
    //             var name = row.find("[name='FILE']").html();
    //             list += id+":"+name;});
    for (var i = 1; i < tableObj.rows.length; i++) {    //遍历Table的所有Row
        for (var j = 0; j < tableObj.rows[i].cells.length; j++) {   //遍历Row中的每一列
            if (j==2){
                tableInfo += tableObj.rows[i].cells[j].children[0].checked;
                tableInfo += tableObj.rows[i].cells[j].children[1].checked;
                tableInfo += ";"
            }
            else tableInfo += tableObj.rows[i].cells[j].innerText+";";   //获取Table中单元格的内容
            tableInfo += "   ";
        }
        tableInfo += "\n";
    }
    formdata.append("table",tableInfo);
    $.ajax({
        url: "/PostData",
        type: "post",
        data: formdata,
        contentType: false,
        processData: false,
        success: function (data) {
            alert("信息上传成功！")
        },
        error: function (data) {
            alert("信息上传失败！");
            console.log(data)
        }
    })
}

function mulval(id) {
    $.ajax({
        url: "/GenMulval",
        type: "post",
        data: "hello",
        contentType: false,
        processData: false,
        success: function (data) {
            alert("攻击图生成成功！")
        },
        error: function (data) {
            alert("攻击图生成失败！");
            console.log(data)
        }
    })
}


