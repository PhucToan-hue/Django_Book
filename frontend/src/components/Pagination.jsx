function Pagination({ currentPage, totalPages, hasNext, hasPrevious, onPageChange }) {
  return (
    <div className="pagination">
      <button type="button" className="secondary" onClick={() => onPageChange(currentPage - 1)} disabled={!hasPrevious}>
        Previous
      </button>

      <div className="pagination-status">
        Trang <strong>{currentPage}</strong> / {totalPages || 1}
      </div>

      <button type="button" className="secondary" onClick={() => onPageChange(currentPage + 1)} disabled={!hasNext}>
        Next
      </button>
    </div>
  );
}

export default Pagination;
