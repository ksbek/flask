// custom javascript
function urlify(str) {
	var urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
	return str.replace(urlRegex, '<a href="$1" class="exturl">$1</a>');
}

function getDocument() {
	$("#titleList tbody tr").click(function() {
		$("#titleList tbody tr").each(function() {
			$(this).removeClass('selected');
		});
		$(this).addClass('selected');
		$.ajax({
		  method: "GET",
		  url: "/documents/" + $(this).attr("id")
		}).done(function( response ) {
			var result = JSON.parse(response);
			$("#addTitleModal").modal("hide");
			if(result.success) {
				$("#documentNotes").html(result.data.notes);
				$("#documentID").val(result.data.id);
				$("#createdDate").html(result.data.created_on);
				$("#updatedDate").html(result.data.modified_on);
				$("#authorName").html(result.data.author);
				$("#editorName").html(result.data.editor);
			}
		});
	});
}

function getUser() {
	$("#userList .edit-user").click(function(event) {
		$("#userID").val($(this).attr("id"));
		$("#addUserModal").modal();
		$.ajax({
		  method: "GET",
		  url: "/users/" + $(this).attr("id")
		}).done(function( response ) {
			var result = JSON.parse(response);
			if(result.success) {
				$("#userEmail").val(result.data.email);
				$("#userName").val(result.data.name);
			}
		});
	});
}

$(document).ready(function(){
	// Get document by ID
	getDocument();
	getUser();
	// Open create docuemt modal
	$("#addTitleBtn").click(function() {
		$("#addTitleModal").modal();
	});

	// Add document
	$("#addTitleSubmitBtn").click(function(event) {
		event.preventDefault();
		var data = {
			title: $("#title").val(),
			subtitle: $("#subtitle").val(),
			notes: $("#notes").val(),
		};
		$.ajax({
		  method: "POST",
		  url: "/documents",
		  data: data
		}).done(function( response ) {
			var result = JSON.parse(response);
			$("#addTitleModal").modal("hide");
			if(result.success) {
				if ($("#documentContent")) {
					$("#documentContent").show();
				}
				$("#titleList tbody tr").each(function() {
					$(this).removeClass('selected');
				});
				$("#titleList tbody").append("<tr id=" + result.data.id +  " class=\"selected\"><td>" + result.data.title + "</td><td>" + result.data.subtitle + "</td></tr>")
				$("#documentNotes").html(result.data.notes);
				$("#documentID").val(result.data.id);
				$("#createdDate").html(result.data.created_on);
				$("#updatedDate").html(result.data.modified_on);
				$("#authorName").html(result.data.author);
				$("#editorName").html(result.data.editor);
				getDocument();
			}
		});
	});

	// Update document
	$("#updateTitleBtn").click(function(event) {
		var data = {
			id: $("#documentID").val(),
			notes: $("#documentNotes").html()
		};
		$.ajax({
		  method: "PUT",
		  url: "/documents",
		  data: data
		}).done(function( response ) {
			var result = JSON.parse(response);
			if(result.success) {
				$("#createdDate").html(result.data.created_on);
				$("#updatedDate").html(result.data.modified_on);
				$("#authorName").html(result.data.author);
				$("#editorName").html(result.data.editor);
			}
		});
	});

	// Open update user modal
	$("#addUserBtn").click(function() {
		$("#userID").val('');
		$("#userEmail").val('');
		$("#userName").val('');
		$("#userPassword").val('');
		$("#addUserModal").modal();
	});

	// Add user
	$("#addUserSubmitBtn").click(function(event) {
		event.preventDefault();
		var method = 'POST';
		var url = 'users'		
		var data = {
			email: $("#userEmail").val(),
			name: $("#userName").val(),
			password: $("#userPassword").val(),
			confirm: $("#userPassword").val()
		};
		if ($("#userID").val() != '' && $("#userID").val() != undefined) {
			method = 'PUT';
			data.id = $("#userID").val();
		}
		$.ajax({
		  method: method,
		  url: url,
		  data: data
		}).done(function( response ) {
			var result = JSON.parse(response);
			$("#addUserModal").modal("hide");
			if(result.success) {
				var html = "<tr id='user" + result.data.id + "'>" + 
						"<td>" + result.data.email + "</td>" + 
						"<td>" + result.data.name + "</td>" + 
						"<td><button class='btn btn-sm btn-primary edit-user' id='" + result.data.id + "'>Edit</button></td>" + 
						"</tr>";
				if (method == 'POST')
					$("#userList").append(html);
				else
					$("tr#user" + result.data.id).replaceWith(html);
				getUser();
			} else {
				alert(result.message)
			}
		});
	});
});