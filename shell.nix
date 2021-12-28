{ pkgs ? import <nixpkgs> {} }:

with pkgs;
let
  snapfaas = import (fetchFromGitHub {
    owner = "princeton-sns";
    repo = "snapfaas";
    rev = "d9da995d2b72ccfc5fe18500c2e71d8a1dff7c21";
    sha256 = "08lsw6sslfvpy461cgdas3hqk226yzhyffr4q87cgc2w940vnxc4";
  }) { inherit pkgs; release = false; };
in mkShell {
  buildInputs = [ lkl snapfaas ];
  shellHook = ''
    # Mark variables which are modified or created for export.
    set -a
    source ${toString ./.env}
    set +a
  '';
}
