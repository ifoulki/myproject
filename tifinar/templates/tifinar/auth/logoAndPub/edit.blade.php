<x-layoutAdm page='تعديل كتاب : {{$book->title}}'>

	<section class="content">

		<article class="content">

			<h1>
				<i class="fas fa-edit"></i> تعديل كتاب: <br> {{$book->title}}
			</h1>

			<form method="POST" action="{{route('books.update', $book)}}" enctype="multipart/form-data">
				@csrf
				@method('PUT')

				@if($book->Myimage)
					<img id="imagePreview" src="{{ asset('images/books/'.$book->Myimage) }}" class="image-preview" alt="معاينة الصورة">
				@else
					<img id="imagePreview" class="image-preview" alt="معاينة الصورة" style="display: none;">
				@endif

				<br>
				<label class="label">
					<i class="fas fa-upload"></i> تعديل الصورة:
				</label>

				<div class="mb-3">
					<input class="form-control" type="file" id="formFile" name="Myimage">
				</div>

				<hr>

				<div class="form-group">
					<label class="label" for="title"><i class="fas fa-heading"></i> عنوان الكتاب:</label>
					<input
						required
						type="text"
						id="title"
						name="title"
						placeholder="عنوان المنشور ..."
						minlength="7"
						class="title form-control"
						value="{{$book->title}}"
					>
				</div>
	
				<hr>
	
				<div class="form-group">
					<label class="label" for="author"><i class="fas fa-user"></i> اسم الكاتب:</label>
					<input
						required
						type="text"
						id="author"
						name="author"
						placeholder="اسم الكاتب ..."
						minlength="5"
						class="author form-control"
						value="{{$book->Author}}"
					>
				</div>
	
				<hr>
	
				<div class="form-group">
					<label class="label" for="Mysubject"><i class="fas fa-file-alt"></i> ملخص موجز عن الكتاب:</label>
					<textarea
						required
						id="Mysubject"
						name="Mysubject"
						minlength="100"
						class="Mysubject"
						placeholder="اكتب ملخص موجز عن الكتاب هنا..."
					>{{$book->Mysubject}}</textarea>
				</div>
	
				<hr>
	
				<div class="form-group">
					<label class="label " for="the_type"><i class="fas fa-tag"></i> نوع المنشور:</label>
					<select class="form-control form-select" id="the_type" name="the_type" required>
						<option value="" disabled {{ $book->the_type == '' ? 'selected' : '' }}>اختر نوع المنشور...</option>
	
						<optgroup label="اللغات:">
							<option value="الأمازيغية" {{$book->the_type == 'الأمازيغية' ? 'selected' : ''}}>تعلم الأمازيغية</option>
							<option value="Apprendre le français" {{$book->the_type == 'Apprendre le français' ? 'selected' : ''}}>تعلم الفرنسية</option>
							<option value="Learn English" {{$book->the_type == 'Learn English' ? 'selected' : ''}}>تعلم الإنجليزية</option>
						</optgroup>
	
						<optgroup label="العلوم:">
							<option value="علوم Apprendre les maths" {{$book->the_type == 'علوم Apprendre les maths' ? 'selected' : ''}}>تعلم الرياضيات</option>
							<option value="علوم الفزياء والكيمياء" {{$book->the_type == 'علوم الفزياء والكيمياء' ? 'selected' : ''}}>الفزياء والكيمياء</option>
							<option value="علوم الحياة والأرض SVT" {{$book->the_type == 'علوم الحياة والأرض SVT' ? 'selected' : ''}}>علوم الحياة والأرض</option>
						</optgroup>
	
						<optgroup label="مواضيع أخرى:">
							<option value="صحة وحياة" {{$book->the_type == 'صحة وحياة' ? 'selected' : ''}}>صحة وحياة</option>
							<option value="Computer Science علوم الحاسوب" {{$book->the_type == 'Computer Science علوم الحاسوب' ? 'selected' : ''}}>علوم الحاسوب</option>
							<option value="القانون وحقوق الإنسان" {{$book->the_type == 'القانون وحقوق الإنسان' ? 'selected' : ''}}>القانون وحقوق الإنسان</option>
							<option value="الثقافة العامة" {{$book->the_type == 'الثقافة العامة' ? 'selected' : ''}}>الثقافة العامة</option>
							<option value="تربية وتعليم" {{$book->the_type == 'تربية وتعليم' ? 'selected' : ''}}>تربية وتعليم</option>
							<option value="أصناف أخرى" {{$book->the_type == 'أصناف أخرى' ? 'selected' : ''}}>أصناف أخرى</option>
						</optgroup>
	
						@if (!in_array($book->the_type, ['الأمازيغية', 'Apprendre le français', 'Learn English', 'علوم Apprendre les maths', 'علوم الفزياء والكيمياء', 'علوم الحياة والأرض SVT', 'صحة وحياة', 'Computer Science علوم الحاسوب', 'القانون وحقوق الإنسان', 'الثقافة العامة', 'تربية وتعليم', 'أصناف أخرى']))
							<option value="{{ $book->the_type }}" selected>{{ $book->the_type }}</option>
						@endif
					</select>
				</div>
				
				<hr>
	
				<div class="form-group">
					<label class="label" for="Mydescription"><i class="fas fa-info-circle"></i> وصف المنشور:</label>
					<textarea
						required
						id="Mydescription"
						name="Mydescription"
						class="description"
						placeholder="أكتب وصفاً لمنشورك..."
					>{{$book->Mydescription}}</textarea>
				</div>
		
				<hr>
		
				<div class="form-group">
					<label class="label" for="Keyword"><i class="fas fa-key"></i> الكلمات المفتاحية:</label>
					<textarea
						id="Keyword"
						name="Keyword"
						class="Keyword"
						placeholder="الكلمات المفتاحية..."
					>{{$book->Keyword}}</textarea>
				</div>
		
				<hr>
		
				<div class="form-group">
					<button type="submit" class="btn add_btn form-control"><i class="fas fa-save"></i> تحديث الكتاب</button>
				</div>
			</form>

			@include('auth.books.edditComments')
		</article>
	
	</section>

	<script>

		document.getElementById('formFile').addEventListener('change', function(event) {
			const file = event.target.files[0];
			const preview = document.getElementById('imagePreview');
				
			if (file) {
				const reader = new FileReader();
				reader.onload = function(e) {
					preview.src = e.target.result;
					preview.style.display = 'block';
				}

				reader.readAsDataURL(file);
			} else {
				preview.src = '';
				preview.style.display = 'none';
			}
		});
    </script>

</x-layoutAdm>
	