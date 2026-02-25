// Filter and search functionality
(function() {
    // DOM elements
    const searchInput = document.getElementById('search');
    const minQtyInput = document.getElementById('min_qty');
    const maxQtyInput = document.getElementById('max_qty');
    const filterToggle = document.getElementById('filterToggle');
    const filterPanel = document.getElementById('filterPanel');
    const clearFiltersBtn = document.getElementById('clearFiltersBtn');
    const itemsList = document.getElementById('itemsList');
    const itemCount = document.getElementById('itemCount');
    const itemLabel = document.getElementById('itemLabel');
    const emptyState = document.getElementById('emptyState');

    // Check if all required elements exist
    if (!searchInput || !itemsList) {
        console.warn('Required filter elements not found');
        return;
    }

    // Filter toggle functionality
    if (filterToggle && filterPanel) {
        filterToggle.addEventListener('click', function(e) {
            e.preventDefault();
            filterPanel.classList.toggle('hidden');
            filterToggle.classList.toggle('bg-blue-500');
            filterToggle.classList.toggle('bg-gray-500');
            filterToggle.classList.toggle('hover:bg-blue-600');
            filterToggle.classList.toggle('hover:bg-gray-600');
        });
    }

    // Apply filters function - filters items based on search and quantity criteria
    function applyFilters() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const minQty = minQtyInput.value ? parseInt(minQtyInput.value) : 0;
        const maxQty = maxQtyInput.value ? parseInt(maxQtyInput.value) : Infinity;

        // Get all item rows
        const itemRows = itemsList.querySelectorAll('.item-row');
        let visibleCount = 0;

        itemRows.forEach(row => {
            const name = row.dataset.name.toLowerCase();
            const qty = parseInt(row.dataset.qty);

            // Check if item matches all filters
            const matchesSearch = name.includes(searchTerm);
            const matchesQtyRange = qty >= minQty && qty <= maxQty;

            if (matchesSearch && matchesQtyRange) {
                row.style.display = '';
                visibleCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Update item count and label
        if (itemCount) {
            itemCount.textContent = visibleCount;
        }
        if (itemLabel) {
            const pluralForm = visibleCount === 1 ? 'item' : 'items';
            itemLabel.textContent = pluralForm;
        }

        // Show/hide empty state and list
        if (visibleCount === 0) {
            if (emptyState) emptyState.style.display = 'block';
            itemsList.style.display = 'none';
            if (itemCount && itemCount.parentElement) {
                itemCount.parentElement.style.display = 'none';
            }
        } else {
            if (emptyState) emptyState.style.display = 'none';
            itemsList.style.display = '';
            if (itemCount && itemCount.parentElement) {
                itemCount.parentElement.style.display = 'block';
            }
        }
    }

    // Search input event listener - triggers on keyup and checks for minimum 3 characters
    searchInput.addEventListener('keyup', function(event) {
        const currentValue = searchInput.value.trim();
        
        // Only filter if we have 0 or 3+ characters (allows clearing filter)
        if (currentValue.length === 0 || currentValue.length >= 3) {
            applyFilters();
        }
    });

    // Quantity filter event listeners - trigger on any change
    if (minQtyInput) {
        minQtyInput.addEventListener('input', applyFilters);
    }
    if (maxQtyInput) {
        maxQtyInput.addEventListener('input', applyFilters);
    }

    // Clear filters button
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            searchInput.value = '';
            if (minQtyInput) minQtyInput.value = '';
            if (maxQtyInput) maxQtyInput.value = '';
            applyFilters();
        });
    }

    // Initial render - show all items on page load
    applyFilters();
})();
