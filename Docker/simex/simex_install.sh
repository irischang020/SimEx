BRANCH=docker
URL=https://github.com/eucall-software/simex_platform/archive/${BRANCH}.zip


cd /opt

wget $URL
unzip ${BRANCH}.zip
rm ${BRANCH}.zip
cd simex_platform-${BRANCH}


export BOOST_ROOT=/opt/boost
export Boost_NO_SYSTEM_PATHS=ON
#export ARMA_DIR=/usr

export PATH=/opt/miniconda2/bin:$PATH
export HDF5_ROOT=/opt/miniconda2

ROOT_DIR=/opt/simex_platform
mkdir -p $ROOT_DIR
# Create new build dir and cd into it.

mkdir -v build
cd build

# Uncomment the next line and specify the install dir for a custom user install.
#cmake -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR
# Uncomment the next line and specify the install dir for a developer install.
cmake -DSRW_OPTIMIZED=ON -DDEVELOPER_INSTALL=OFF -DCMAKE_INSTALL_PREFIX=$ROOT_DIR $ROOT_DIR ..

chmod og+rwX -R $ROOT_DIR

# Build the project.
make -j8


# Install the project.
make install
cd ../..

rm -rf simex_platform-${BRANCH}


#remove tests?
rm -rf $ROOT_DIR/Tests

echo "source /opt/simex_platform/bin/simex_vars.sh" > /etc/profile.d/scripts-simex.sh && \
	chmod 755 /etc/profile.d/scripts-simex.sh
chmod og+rwX -R /opt/simex_platform

