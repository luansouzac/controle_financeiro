import { createStore } from 'vuex';

export default createStore({
  state: {
    transactions: [],
    balance: 0,
  },
  mutations: {
    addTransaction(state, transaction) {
      state.transactions.push(transaction);
      state.balance += transaction.amount;
    },
    removeTransaction(state, transactionId) {
      const transactionIndex = state.transactions.findIndex(t => t.id === transactionId);
      if (transactionIndex !== -1) {
        state.balance -= state.transactions[transactionIndex].amount;
        state.transactions.splice(transactionIndex, 1);
      }
    },
    setBalance(state, newBalance) {
      state.balance = newBalance;
    },
  },
  actions: {
    addTransaction({ commit }, transaction) {
      commit('addTransaction', transaction);
    },
    removeTransaction({ commit }, transactionId) {
      commit('removeTransaction', transactionId);
    },
    updateBalance({ commit }, newBalance) {
      commit('setBalance', newBalance);
    },
  },
  getters: {
    allTransactions: (state) => state.transactions,
    currentBalance: (state) => state.balance,
  },
});