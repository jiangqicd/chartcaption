<template>
    <div>
      <button @click="fetchData">获取数据</button>
      <textarea v-model="displayText" readonly></textarea>
    </div>
  </template>
   
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        books: [],  // 用于存储书籍数据
        displayText: "", // 用于在文本框中显示的文本
      };
    },
    methods: {
      fetchData() {
        let url = "/books";
        axios
          .post("/api" + url, {
            a: 1,
            b: 2,
            c: "你好",
          })
          .then((res) => {
            this.books = res.data.books; // 假设后端返回的书籍数组在 res.data.books 中
            console.log(res.data)
            console.log(res.data.books)
            console.log(this.books)
            this.formatDisplayText();
          })
          .catch((error) => {
            console.error(error);
          });
      },
      formatDisplayText() {
        // 将书籍数据格式化为字符串
        this.displayText = this.books.map(book => `书名：${book.title}，作者：${book.author}`).join('\n');
      },
    }
  };
  </script>