app=${PWD##*/}

echo "=== PRE-FLIGHT CHECKS AND VERSION BUMP ==="

if [ -n "$(git status --porcelain library)" ]; then
  echo "library folder is not clean. Cannot continue.";
  exit 1
fi

if [ -n "$(git status --porcelain . | grep -v / | grep -v release.sh)" ]; then
  echo "Top level directory is not clean. Cannot continue.";
  exit 1
fi

# if [ -n "$(flake8 --max-line-length=160 --ignore=W503,W606,E226 library)" ]; then
#  echo "There are flake8 issues; code style is bad";
#  exit 1
#fi

if [ -z "${1}" ]; then
    echo "Argument required specifying version number"
    echo "current version number is `cat library/version.txt`"
    exit 1
fi
version="${1}"

printf "${version}" > library/version.txt
# sed "s/library==version/library==${version}/g" requirements_library.template > requirements_library.txt
git add library/version.txt
git add requirements_library.txt
git commit -m "release.sh: version bump ${version}"

echo "======================"
echo "=== RELEASE FOR $app - ${1}"
echo "======================"

./build.sh
if [ "$?" != 0 ]; then
    exit 1
fi

echo "=== BUILDING PYTHON PACKAGE ==="
python setup.py sdist
if [ "$?" != 0 ]; then
    echo "*** FAILED with code $test_exit_code ***"
    exit 2
fi


echo "=== TESTING LOCAL PYTHON PACKAGE ==="
./acctest_python_package_local.sh
test_exit_code=$?
if [ "$test_exit_code" = 0 ]; then
    echo "*** LOCAL PACKAGE TEST PASSED ***"
else
    echo "*** LOCAL PACKAGE TEST FAILED ***"
    exit 5
fi

echo "=== UPLOADING PYTHON PACKAGE TO GEMFURY ==="
curl_result=$(curl -F package=@dist/library-${version}.tar.gz https://FqvvdcgGB6UeUJ8VYDmr@push.fury.io/combiz/)
if [ "$?" != 0 ]; then
    echo "*** FAILED for version=${version} ***"
    exit 3
fi
if [ `echo $curl_result | grep 'version already exists' | wc -l` != 0 ] ; then
    echo "*** FAILED for version=${version} version already exists ***"
    exit 4
fi

sleep 10

echo "=== TESTING REMOTE PYTHON PACKAGE ==="
./acctest_python_package.sh
test_exit_code=$?
if [ "$test_exit_code" = 0 ]; then
    echo "*** PACKAGE TEST PASSED ***"
else
    echo "*** PACKAGE TEST FAILED ***"
    exit 5
fi

echo "=== CREATING GIT TAG ==="
git tag -a ${version} -m "${version} from release.sh"
if [ "$?" != 0 ]; then
    echo "*** TAGGING FAILED ***"
    exit 6
fi

./build_library_docker.sh
if [ "$?" != 0 ]; then
    echo "*** BUILDING DOCKER IMAGE FAILED (${?}) ***"
    exit 7
fi

echo ""
echo "=== SUCCESS ==="