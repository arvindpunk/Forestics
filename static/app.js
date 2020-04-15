var app = new Vue({
  el: '#app',
  delimiters: ['[[',']]'],     
  data: {
    message: 'Hello Vue!',
    lat: '',
    lng: '',
    images: [],
    name: '',
    success: false

  },
  methods: {
    addLocation(){
      fetch('http://127.0.0.1:5000/addnew?lat=' + this.lat + '&lng=' + this.lng + '&name=' + this.name);

      this.lat = '';
      this.lng = '';
      this.name = '';
      this.success = true;

    }
  },
  async created(){
    let res = await fetch('http://127.0.0.1:5000/getpaths');
    this.images = await res.json();
    console.log(this.images)
  }
})