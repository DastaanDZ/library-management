<template>
  <div>
    <h1>Monitored Books</h1>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Book Name</th>
          <th scope="col">Availability</th>
          <th scope="col">Users Issued To</th>
          <!-- New column for actions -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="(book, index) in monitoredBooks" :key="index">
          <td>{{ book.name }}</td>
          <td
            :class="{
              'text-success': book.available,
              'text-danger': !book.available,
            }"
          >
            {{ book.available ? "Available" : "Issued" }}
          </td>
          <td>
            <template v-if="book.users_issued_to.length > 0">
              <div v-for="(user, i) in book.users_issued_to" :key="i">
                <div>{{ user.name }}</div>
                <div
                  v-if="i !== book.users_issued_to.length - 1"
                  class="line-break"
                ></div>
                <!-- Add line break if not the last user -->
                <button
                  @click="revokeAccess(book.id, user.id)"
                  class="btn btn-danger"
                >
                  Revoke
                </button>
              </div>
            </template>

            <template v-else> No users issued </template>
          </td>
          <td>
            <!-- Placeholder for actions when no users issued -->
          </td>
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
        this.monitoredBooks = response.data;
        console.log(this.monitoredBooks);
      } catch (error) {
        console.error("Error fetching monitored books:", error);
      }
    },
    async revokeAccess(bookId, userId) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.post(
          "http://127.0.0.1:5000/revoke-access",
          {
            book_id: bookId,
            user_id: userId,
          },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        alert("Access revoked for user");
        this.fetchMonitoredBooks();

        console.log(response.data.message); // Log the response message
        // Optionally, you can update the UI or perform any other actions after revoking access
      } catch (error) {
        console.error("Error revoking access:", error);
        // Handle errors here
      }
    },
  },
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.table th {
  background-color: #f8f9fa;
}

.text-success {
  color: #28a745;
}

.text-danger {
  color: #dc3545;
}
.line-break {
  margin-bottom: 5px; /* Adjust the spacing as needed */
}
</style>
