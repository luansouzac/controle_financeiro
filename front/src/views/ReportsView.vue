<template>
  <div class="reports-view">
    <h1>Financial Reports</h1>
    <p>Here you can view and analyze your financial reports.</p>
    <div class="report-list">
      <!-- Placeholder for report items -->
      <div class="report-item" v-for="report in reports" :key="report.id">
        <h2>{{ report.title }}</h2>
        <p>{{ report.description }}</p>
        <button @click="viewReport(report.id)">View Report</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ReportsView',
  data() {
    return {
      reports: [
        { id: 1, title: 'Monthly Summary', description: 'Overview of the monthly financial activities.' },
        { id: 2, title: 'Annual Report', description: 'Detailed report of the annual financial performance.' },
        { id: 3, title: 'Expense Breakdown', description: 'Analysis of expenses over the selected period.' },
      ],
    };
  },
  methods: {
    viewReport(reportId: number) {
      // Logic to view the selected report
      console.log(`Viewing report with ID: ${reportId}`);
    },
  },
});
</script>

<style scoped>
.reports-view {
  padding: 20px;
}

.report-list {
  margin-top: 20px;
}

.report-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}

.report-item h2 {
  margin: 0;
}

.report-item button {
  margin-top: 10px;
}
</style>