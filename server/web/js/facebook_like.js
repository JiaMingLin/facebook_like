var base_url = window.parent.$('#base_url').val();
var table
var index = 0
var post_url = base_url + 'get_posts'
var get_like_url = base_url + 'get_likes'
function getPosts(page_name, search_str, more_data){
	if(more_data){
		index += 1
		append_more_data(page_name, search_str)
	}else{
		index = 0
		get_new_data(page_name, search_str)
	}
}

function get_new_data(page_name, search_str){
	$.ajax({
		method: 'POST',
		data:{
			'page_name': page_name,
			'search_str': search_str
		},
		dataType: 'json',
		url: post_url,
		success: function(result){
			var dataSet = result.data
			var cols = result.columns
			clear()
			table = $("#data_table").DataTable({
				data: dataSet,
				paging: false,
				searching: true,
				columns: cols,
				order: [
					[0, 'desc']
				],
				columnDefs:[
					{
						targets: [1],
						visible: false
					}

				]
			});

			$('#data_table tbody').on( 'click', 'tr', function () {
				if ( $(this).hasClass('selected') ) {
					$(this).removeClass('selected');
				}
				else {
					table.$('tr.selected').removeClass('selected');
					$(this).addClass('selected');
				}
				
				var row_data = table.row('.selected').data()
				var selected_id = row_data[1]
				//console.log(selected_id)

				window.parent.frames['like_list'].get_likes(selected_id);
			});
			$('#more_posts').show()
		}
	});
}

function append_more_data(page_name, search_str){
	$.ajax({
		method: 'POST',
		data:{
			'page_name': page_name,
			'search_str': search_str,
			'index': index
		},
		dataType: 'json',
		url: post_url,
		success: function(result){
			var dataSet = result.data
			var cols = result.columns

			for (var y = 0; y < dataSet.length; y++) {
				table.row.add(dataSet[y]).draw();
			}
		}
	});
}

function get_likes(post_id){
	$.ajax({
		method: 'POST',
		data:{
			'post_id': post_id
		},
		dataType: 'json',
		url: get_like_url,
		success: function(result){
			var dataSet = result.data
			var cols = result.columns
			var counts = result.counts
			var path = result.path
			var download_path = base_url + 'web/'+path
			$("#post_id").text(post_id)
			$("#counts").text(counts)
			$("#download_link").attr("href", download_path);
			$("#download_link").css("display", "block");
			table = $("#data_table").DataTable({
				destroy: true,
				data: dataSet,
				paging: false,
				searching: false,
				columns: cols,
			});
		}
	});
}

function clear(){
	if($.fn.DataTable.isDataTable( '#data_table' )){
		table.clear().draw()
		table.destroy()
		table = null
		$('#data_table').empty()
	}
	if($("#download_link")){
		$("#download_link").css("display", "none");
	}
}
