{% extends "main.tpl" %}
{% block body %}

	<header>
		<div class="logo-wrap">
			<div class="container">
				<div class="row justify-content-between align-items-center">
					<div class="col-lg-4 col-md-4 col-sm-12 logo-left no-padding">
						<a href="/">
							<img class="img-fluid" src="web/img/logo.png" alt="">
						</a>
					</div>
					<div class="col-lg-8 col-md-8 col-sm-12 logo-right no-padding ads-banner">
						<img class="img-fluid" src="web/img/banner-ad.jpg" alt="">
					</div>
				</div>
			</div>
		</div>
		{% block menu %}{% endblock menu %}
	</header>

	{% block container %}{% endblock container %}

	{% block js %}{% endblock js %}

{% endblock body %}
