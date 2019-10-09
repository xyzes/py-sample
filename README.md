# PySample
<h3>a multimedia library management solution</h3>

<h6>Introduction</h6>
<p>This project is a <strong>Python + Flask</strong> web application to manage, store, and edit metadata of multimedia files through the use of a database.
Features of the program will include:</p>
<div>
  <ol> 
    <li><strong>Real-time scanning of user library</strong>. Add new entries for new files, show missing files.</li>
    <li>Perform two-way <strong>CRUD operations</strong> (database changes trigger changes in file system and viceversa).</li>
    <li>Handle complex requests, like <strong>finding files with empty fields</strong> or <strong>finding duplicates</strong>.</li>
    <li>A <strong> web interface</strong> to view the database and <strong>command changes in the file system</strong>.</li>
  </ol>
</div>
<p>Originally intended as an application to allow music producers, DJ's, and other digital music workers to better organize their files safely and efficiently through its minimalistic interface, its final state will support other types of multimedia as well. <strong>This is a long-term project and is intended to become a full multimedia managament software application.</strong></p>

<h6>Contents</h6>
<ul>
  <li><strong>/data</strong> folder contains .bacpac self-contained Microsoft SQL Server database (developed using SQL Server Management Studio).</li>
  <li><strong>/media</strong> folder contains pictures of the database design and screenshots showing the current state of the project.</li>
  <li><strong>/py-sample</strong> folder contains three important .py files, essential for functionality of the project:
  <ol>
    <li><strong>__init__.py</strong> - Initializes the application & development server.</li>
    <li><strong>utils.py</strong> - Contains controller and helpers to handle input from GUI, issue queries to the database, interpret the data received and convert it to appropriate format.</li>
    <li><strong>views.py</strong> - Handles the different views and components of the web application. </li>
  </ol>
  </li>
</ul>
  
