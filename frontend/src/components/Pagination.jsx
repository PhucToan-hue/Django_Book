function Pagination({ currentPage, totalPages, hasNext, hasPrevious, onPageChange }) {
  const firstPage = Math.max(1, Math.min(currentPage - 1, totalPages - 2));
  const visiblePages = Array.from(
    { length: Math.min(3, totalPages) },
    (_, index) => firstPage + index,
  );

  return (
    <div className="pagination">
      <button type="button" className="secondary" onClick={() => onPageChange(currentPage - 1)} disabled={!hasPrevious}>
        Previous
      </button>

      <div className="pagination-status" aria-label={`Trang ${currentPage} trên ${totalPages}`}>
        {visiblePages.map((pageNumber) => (
          <button
            key={pageNumber}
            type="button"
            className={pageNumber === currentPage ? '' : 'secondary'}
            onClick={() => onPageChange(pageNumber)}
            aria-current={pageNumber === currentPage ? 'page' : undefined}
          >
            {pageNumber}
          </button>
        ))}
      </div>

      <button type="button" className="secondary" onClick={() => onPageChange(currentPage + 1)} disabled={!hasNext}>
        Next
      </button>
    </div>
  );
}

export default Pagination;
