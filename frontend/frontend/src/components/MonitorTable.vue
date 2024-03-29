<template>
  <div>
    <h1>Monitored Books</h1>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Book Name</th>
          <th scope="col">User Name</th>
          <th scope="col">Issue Date</th>
          <th scope="col">Return Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(book, index) in monitoredBooks" :key="index">
          <td>{{ book.book_name }}</td>
          <td>{{ book.user_name }}</td>
          <td>{{ book.issue_date }}</td>
          <td>{{ book.return_date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MonitoredBooks",
  data() {
    return {
      monitoredBooks: [],
    };
  },
  mounted() {
    this.fetchMonitoredBooks();
  },
  methods: {
    async fetchMonitoredBooks() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/monitor", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        });
        this.monitoredBooks = response.data.monitored_books;
      } catch (error) {
        console.error("Error fetching monitored books:", error);
      }
    },
  },
};
</script>

<style>
/* Add your styles here */
</style>
