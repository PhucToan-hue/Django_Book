function BookFilter({ filters, setFilters, pageSize, onPageSizeChange, onSubmit, onReset }) {
  const handleChange = (event) => {
    const { name, value } = event.target;

    setFilters((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  return (
    <form className="filter-bar" onSubmit={onSubmit}>
      <label>
        <span>Title</span>
        <input name="title" value={filters.title} onChange={handleChange} placeholder="Tìm theo title" />
      </label>

      <label>
        <span>Author</span>
        <input name="author" value={filters.author} onChange={handleChange} placeholder="Tìm theo author" />
      </label>

      <label>
        <span>Page size</span>
        <select value={pageSize} onChange={(event) => onPageSizeChange(Number(event.target.value))}>
          <option value={10}>10 record</option>
          <option value={20}>20 record</option>
          <option value={50}>50 record</option>
          <option value={100}>100 record</option>
        </select>
      </label>

      <button type="submit">Lọc</button>
      <button type="button" className="secondary" onClick={onReset}>
        Đặt lại
      </button>
    </form>
  );
}

export default BookFilter;
