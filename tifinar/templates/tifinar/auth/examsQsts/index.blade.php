<x-layoutAdm page='إدارة الأسئلة'>

    <section class="content">
        <div class="container">
            <h1>قائمة الأسئلة</h1>

            @if (session('success'))
                <div class="alert alert-success">
                    {{ session('success') }}
                </div>
            @endif

            <a href="{{ route('examItems.create') }}" class="btn btn-primary mb-3">إضافة سؤال جديد</a>

            <form action="{{ route('examItems.index') }}" method="GET" class="mb-4">
                <div class="form-group">
                    <label for="exam_number">فلترة حسب عنوان الاختبار:</label>
                    <select class="form-control" name="exam_number">
                        <option value="" disabled selected>حدد الاختبار</option>
                        @foreach ($exams as $exam)
                            <option value="{{ $exam->exam_id }}" 
                                {{ request('exam_number') == $exam->exam_id ? 'selected' : '' }}>
                                {{ $exam->title }}
                            </option>
                        @endforeach
                    </select>
                </div>
                <button type="submit" class="btn btn-secondary">بحث</button>
                <a href="{{ route('examItems.index') }}" class="btn btn-light">إلغاء التصفية</a>
            </form>

            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>الرقم</th>
                        <th>الاختبار التابع له</th>
                        <th>عنوان السؤال</th>
                        <th>النوع</th>
                        <th>العلامة</th>
                        <th>التحكم</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($items as $item)
                        <tr>
                            <td>{{ $item->qsts_id }}</td>
                            <td>{{ $item->exam_number }}</td>
                            <td>{{ $item->qst_1st_line }}</td>
                            <td>{{ $item->the_type }}</td>
                            <td>{{ $item->mark }}</td>
                            <td>

                                <a href="{{ route('examItems.edit', $item->premary_id) }}" class="btn btn-warning">تعديل</a>

                                <form action="{{ route('examItems.destroy', $item->premary_id) }}" method="POST" style="display:inline-block;" onsubmit="return confirm('هل أنت متأكد من الحذف؟')">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" class="btn btn-danger">حذف</button>
                                </form>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="6" class="text-center">لا توجد أسئلة حالياً</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </section>

</x-layoutAdm>
