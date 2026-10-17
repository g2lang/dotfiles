{ lib, appimageTools, fetchurl }:

let
  version = "1.4.229";
  pname = "orca-ide";
  src = fetchurl {
    url = "https://github.com/stablyai/orca/releases/download/v${version}/orca-linux.AppImage";
    sha256 = "033e947e59ddf4f66b751888257dd798f88346db730af186fec94a6e551d7da0";
  };
  appimageContents = appimageTools.extract {
    inherit pname version src;
  };
in
appimageTools.wrapType2 {
  inherit pname version src;

  extraInstallCommands = ''
    install -Dm644 ${appimageContents}/orca-ide.desktop $out/share/applications/orca-ide.desktop
    substituteInPlace $out/share/applications/orca-ide.desktop \
      --replace-fail "Exec=AppRun %U" "Exec=$out/bin/orca-ide %U"
    mkdir -p $out/share/icons
    cp -r ${appimageContents}/usr/share/icons/hicolor $out/share/icons/
  '';

  meta = {
    description = "Desktop orchestrator for AI coding agents";
    homepage = "https://github.com/stablyai/orca";
    license = lib.licenses.mit;
    platforms = [ "x86_64-linux" ];
    mainProgram = "orca-ide";
  };
}
