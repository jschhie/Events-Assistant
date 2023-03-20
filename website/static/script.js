function confirmDelete(delType) {
    if (delType == "single") {
        return confirm('Are you sure you want to delete this item?');
    } else {
        // delType == "all"
        return confirm('Are you sure you want to delete all completed and cancelled items?');
    }
}
