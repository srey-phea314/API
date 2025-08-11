fetch("http://127.0.0.1:8000/products/", {
  method: "GET",
  headers: {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0NzQ2Mjg5LCJpYXQiOjE3NTQ3NDU5ODksImp0aSI6ImE3MTJjNjAzNGNhZTRmMDM5MjAyYWMzN2VlNjAwYzkwIiwidXNlcl9pZCI6IjEifQ.zdO_7LcUyK_biNbWbPXda-ViPrqvcBadKfTkR-itPS"
  }
})
.then(res => res.json())
.then(data => console.log(data));
