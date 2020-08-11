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
  var linelist = JSON.parse(data[key]);
  var x = document.getElementById(id).insertRow(num);
  // x.style.cssText="background-color:#FF0000";
  var c1 = x.insertCell(0);
  var c2 = x.insertCell(1);
  var c3 = x.insertCell(2);
  var c4 = x.insertCell(3);
  var c5 = x.insertCell(4);
  var c6 = x.insertCell(5);
  // c1.style.cssText="border-color:#FF0000";
  // c2.style.cssText="background-color:#FF0000";

  c1.innerHTML = key;
  c2.innerHTML = linelist[0];
  if(linelist[1] === 'N'){
      if(linelist[2] === 'N')
          c3.innerHTML = "<input name='NET' type='checkbox' value=''>网络</input><input name='FILE' type='checkbox' value=''>文件</input>";
      else
          c3.innerHTML = "<input name='NET' type='checkbox' value=''>网络</input><input name='FILE' type='checkbox' checked='checked' value=''>文件</input>";
  }
  else{
      if(linelist[2] === 'N')
          c3.innerHTML = "<input name='NET' type='checkbox' checked='checked' value=''>网络</input><input name='FILE' type='checkbox' value=''>文件</input>";
      else
          c3.innerHTML = "<input name='NET' type='checkbox' checked='checked' value=''>网络</input><input name='FILE' type='checkbox' checked='checked' value=''>文件</input>";
  }
  c4.innerHTML = linelist[3];
  c5.innerHTML = linelist[4];
  c6.innerHTML = linelist[5];
}

function update(id) {
    var formdata = new FormData();
    var tableInfo = [];
    var tableObj = document.getElementById(id);
    for (var i = 1; i < tableObj.rows.length; i++) {    //遍历Table的所有Row
        tableInfo[i-1] = [];
        for (var j = 0; j < tableObj.rows[i].cells.length; j++) {   //遍历Row中的每一列
            if (j===2){
                tableInfo[i-1][2] = [tableObj.rows[i].cells[j].children[0].checked,tableObj.rows[i].cells[j].children[1].checked];
            }
            else tableInfo[i-1][j] = tableObj.rows[i].cells[j].innerText;
        }
    }
    formdata.append("table",JSON.stringify(tableInfo));
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


