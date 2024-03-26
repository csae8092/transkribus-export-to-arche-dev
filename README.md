# transkribus-export-to-arche-dev
repo to develop workflow/scripts to derive arche-metadata from transkribus export documents (mets/page)

## how to export and organize the exported files

* see https://github.com/arthur-schnitzler/schnitzler-zeitungen-static/issues/8#issuecomment-2018591171

* download and unzip the finished downloaded documents
* move the unzipped documents into `export` folder; be aware to only move the folder with named after the document ID and not its root folder with the export id (somehting like `export_job_8515775`)
* your `export` folder should look like
```
├── 1454258
│   └── Wiener_Zeitung_1756-04-17
│       ├── 1454258_0001.jpg
│       ├── 1454258_0002.jpg
│       ├── 1454258_0003.jpg
│       ├── 1454258_0004.jpg
│       ├── 1454258_0005.jpg
│       ├── 1454258_0006.jpg
│       ├── 1454258_0007.jpg
│       ├── 1454258_0008.jpg
│       ├── metadata.xml
│       ├── mets.xml
│       └── page
│           ├── 1454258_0001.xml
│           ├── 1454258_0002.xml
│           ├── 1454258_0003.xml
│           ├── 1454258_0004.xml
│           ├── 1454258_0005.xml
│           ├── 1454258_0006.xml
│           ├── 1454258_0007.xml
│           └── 1454258_0008.xml
└── log.txt
├── the next document id
```

* in order to avoid any file/folder/uri naming issues we need to get rid of the verbose document name folder e.g. `Wiener_Zeitung_1756-04-17`. This can be acchieved by running `python move_files.py`. After running this script you export folder should look like:

```
├── 1454258
│   ├── 1454258_0001.jpg
│   ├── 1454258_0002.jpg
│   ├── 1454258_0003.jpg
│   ├── 1454258_0004.jpg
│   ├── 1454258_0005.jpg
│   ├── 1454258_0006.jpg
│   ├── 1454258_0007.jpg
│   ├── 1454258_0008.jpg
│   ├── metadata.xml
│   ├── mets.xml
│   └── page
│       ├── 1454258_0001.xml
│       ├── 1454258_0002.xml
│       ├── 1454258_0003.xml
│       ├── 1454258_0004.xml
│       ├── 1454258_0005.xml
│       ├── 1454258_0006.xml
│       ├── 1454258_0007.xml
│       └── 1454258_0008.xml
├── 1529236
│   ├── 1529236_0001.jpeg
│   ├── 1529236_0002.jpeg
│   ├── 1529236_0003.jpeg
```

## create ARCHE-Metadata

* adapt [arche_seed_files/arche_constants.ttl](arche_seed_files/arche_constants.ttl) and [arche_seed_files/repo_objects_constants.ttl](arche_seed_files/repo_objects_constants.ttl) to your needs
* run `python make_arche_rdf.py` which writes an `arche.ttl` into this repo`s root directory

## ingest the data

* enter a PHP-ARCHE container `enter_container.sh`
* in the container run `import_metadata.sh`
* after a hopefully succesful import adapat `import_binaries.sh` by adapting your TopCollection URI and execute it

