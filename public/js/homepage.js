function postData(data) {
  $(function() {
    data.forEach(function(article) {
      
    });
  });
}

function check(responseData) {
  if (responseData == "") {
    get('news')
  } else {
    postData(responseData)
  }
}

function get(Data) {
  $(function() {
    $.get(`/${data}`, function (response) {
      check(response)
    })
  })
}

function load() {
  get('news')
}
