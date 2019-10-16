function postData(data, request) {
  $(function() {
    data.forEach(function(article) {
      switch (request) {
        case 'news':
          $('#news').append(`html code to send`);
          break;

        case 'topten':
          $('#topten').append(`html code to send`)
      }
    });
  });
}

function check(responseData, request) {
  if (responseData == "") {
    get('news')
  } else {
    postData(responseData, request)
  }
}

function get(Data) {
  $(function() {
    $.get(`/${data}`, function (response) {
      check(response, data)
    })
  })
}

function load() {
  get('news')
}
