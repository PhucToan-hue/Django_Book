import { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import axiosClient from '../api/axiosClient';
import BookDetail from '../components/BookDetail';
import BookFilter from '../components/BookFilter';
import BookTable from '../components/BookTable';
import Pagination from '../components/Pagination';
import { emptyBookForm } from '../constants/bookForm';

function readBooksResponse(responseData) {
  if (Array.isArray(responseData?.data)) {
    return responseData.data;
  }

  if (Array.isArray(responseData?.results)) {
    return responseData.results;
  }

  if (Array.isArray(responseData?.results?.data)) {
    return responseData.results.data;
  }

  return [];
}

function readBookDetail(responseData) {
  if (responseData?.data && typeof responseData.data === 'object' && !Array.isArray(responseData.data)) {
    return responseData.data;
  }

  return responseData;
}

function HomePage() {
  const navigate = useNavigate();

  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [modalMode, setModalMode] = useState(null);
  const [formData, setFormData] = useState(emptyBookForm);
  const [editingId, setEditingId] = useState(null);
  const [filters, setFilters] = useState({ title: '', author: '' });
  const [appliedFilters, setAppliedFilters] = useState({ title: '', author: '' });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null, totalPages: 1 });
  const [loadingBooks, setLoadingBooks] = useState(false);
  const [savingBook, setSavingBook] = useState(false);
  const [error, setError] = useState('');

  const closeModal = () => {
    setModalMode(null);
    setSelectedBook(null);
  };

  const openCreateModal = () => {
    setEditingId(null);
    setFormData(emptyBookForm);
    setSelectedBook(null);
    setModalMode('create');
    setError('');
  };

  const fetchBooks = useCallback(async () => {
    setLoadingBooks(true);
    setError('');

    try {
      const response = await axiosClient.get('/books/', {
        params: {
          page,
          page_size: pageSize,
          title: appliedFilters.title || undefined,
          author: appliedFilters.author || undefined,
        },
      });

      const responseData = response.data;
      const count = Number(responseData.count || 0);
      const totalPages = Math.max(1, Math.ceil(count / pageSize));

      setBooks(readBooksResponse(responseData));
      setPagination({
        count,
        next: responseData.next,
        previous: responseData.previous,
        totalPages,
      });
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Không thể tải danh sách sách.');
    } finally {
      setLoadingBooks(false);
    }
  }, [appliedFilters.author, appliedFilters.title, page, pageSize]);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  const handleFilterSubmit = (event) => {
    event.preventDefault();
    setPage(1);
    setAppliedFilters(filters);
  };

  const handleFilterReset = () => {
    const resetFilters = { title: '', author: '' };

    setFilters(resetFilters);
    setAppliedFilters(resetFilters);
    setPage(1);
  };

  const handlePageSizeChange = (newPageSize) => {
    setPageSize(newPageSize);
    setPage(1);
  };

  const handleBookSubmit = async (event) => {
    event.preventDefault();
    setSavingBook(true);
    setError('');

    const payload = {
      title: formData.title.trim(),
      author: formData.author.trim(),
      price: Number(formData.price),
      quantity: Number(formData.quantity),
    };

    if (formData.published_date) {
      payload.published_date = formData.published_date;
    }

    try {
      if (editingId) {
        await axiosClient.put(`/books/${editingId}/`, payload);
      } else {
        await axiosClient.post('/books/', payload);
      }

      setFormData(emptyBookForm);
      setEditingId(null);
      closeModal();
      setPage(1);
      await fetchBooks();
    } catch (requestError) {
      const apiErrors = requestError.response?.data?.errors || requestError.response?.data;
      setError(typeof apiErrors === 'string' ? apiErrors : JSON.stringify(apiErrors || 'Không thể lưu sách.'));
    } finally {
      setSavingBook(false);
    }
  };

  const handleDetail = async (bookId) => {
    setError('');

    try {
      const response = await axiosClient.get(`/books/${bookId}/`);
      setSelectedBook(readBookDetail(response.data));
      setModalMode('detail');
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Không thể lấy chi tiết sách.');
    }
  };

  const handleEdit = (book) => {
    setEditingId(book.id);
    setFormData({
      title: book.title || '',
      author: book.author || '',
      price: String(book.price ?? ''),
      quantity: String(book.quantity ?? ''),
      published_date: book.published_date || '',
    });

    setSelectedBook(book);
    setModalMode('edit');
    setError('');
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setFormData(emptyBookForm);
    closeModal();
  };

  const handleDelete = async (book) => {
    const confirmed = window.confirm(`Bạn có chắc muốn xóa sách "${book.title}" không?`);

    if (!confirmed) {
      return;
    }

    try {
      await axiosClient.delete(`/books/${book.id}/`);

      if (books.length === 1 && page > 1) {
        setPage((previousPage) => previousPage - 1);
      } else {
        await fetchBooks();
      }
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Không thể xóa sách.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    navigate('/login', { replace: true });
  };

  const accessToken = localStorage.getItem('accessToken');

  return (
    <main className="app-shell">
      <header className="topbar panel">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Book Management</h1>
          <p className="muted">Quản lý sách với React Vite, token login, filter, pagination và CRUD.</p>
        </div>

        <div className="topbar-actions">
          <button type="button" onClick={openCreateModal}>
            Thêm sách
          </button>
          <span className="token-pill">{accessToken ? 'Authenticated' : 'Guest'}</span>
          <button type="button" className="secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      {error ? <div className="error-box">{error}</div> : null}

      <section className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">Library</p>
            <h2>Danh sách sách</h2>
          </div>
          <div className="stat-pill">Tổng số: {pagination.count} sách</div>
        </div>

        <BookFilter
          filters={filters}
          setFilters={setFilters}
          pageSize={pageSize}
          onPageSizeChange={handlePageSizeChange}
          onSubmit={handleFilterSubmit}
          onReset={handleFilterReset}
        />

        {loadingBooks ? (
          <div className="empty-state">Đang tải dữ liệu...</div>
        ) : (
          <BookTable books={books} onDetail={handleDetail} onEdit={handleEdit} onDelete={handleDelete} />
        )}

        <Pagination
          currentPage={page}
          totalPages={pagination.totalPages}
          hasPrevious={Boolean(pagination.previous)}
          onPageChange={setPage}
        />
      </section>

      <BookDetail
        mode={modalMode}
        book={selectedBook}
        formData={formData}
        setFormData={setFormData}
        editingId={editingId}
        onClose={handleCancelEdit}
        onSubmit={handleBookSubmit}
        onEdit={handleEdit}
        loading={savingBook}
      />
    </main>
  );
}

export default HomePage;
