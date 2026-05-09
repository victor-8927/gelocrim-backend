# Reescreve EntregaScreen como Tela 04 - Detalhes da Parada
conteudo = r"""import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TouchableOpacity, StyleSheet,
  Alert, ActivityIndicator, ScrollView, Image,
  Animated, Linking, FlatList
} from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';

const API_URL = 'https://antsy-gloomily-query.ngrok-free.dev/api/v1';

const TOP_LABEL = {
  '1000': 'Venda', '1009': 'Troca', '1007': 'Bonif.',
  '1008': 'Consig.', '1010': 'Pré-ped.'
};

const PESO_ITEM = { '370': 6, '371': 11, '372': 23, '373': 45 };
const NOME_ITEM = {
  '370': 'GELO 05KG', '371': 'GELO 10KG',
  '372': 'GELO 20KG', '373': 'GELO 40KG'
};

export default function EntregaScreen({ navigation, route }) {
  const { stop, token, routeId, proximoStop } = route.params;
  const [notas, setNotas]       = useState([]);
  const [loadNotas, setLoadNotas] = useState(true);
  const [tela, setTela]         = useState('detalhes'); // detalhes | fotos
  const [acao, setAcao]         = useState(null); // entregar | reentrega | nao_entregue
  const [fotos, setFotos]       = useState({ canhoto: null, outros: [] });
  const [gps, setGps]           = useState(null);
  const [loading, setLoading]   = useState(false);
  const fadeAnim = useRef(new Animated.Value(0)).current;

  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'ngrok-skip-browser-warning': '1'
  };

  useEffect(() => {
    Animated.timing(fadeAnim, { toValue: 1, duration: 300, useNativeDriver: true }).start();
    obterGPS();
    carregarNotas();
  }, []);

  async function obterGPS() {
    try {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') return;
      const loc = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
      setGps(loc.coords);
    } catch {}
  }

  async function carregarNotas() {
    try {
      const res = await fetch(
        `${API_URL}/routes/${routeId}/stops/${stop.stop_id}/notas`,
        { headers }
      );
      if (res.ok) {
        const data = await res.json();
        setNotas(data);
      }
    } catch (e) {
      console.log('Notas erro:', e);
    } finally {
      setLoadNotas(false);
    }
  }

  function abrirMaps() {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${stop.lat},${stop.lng}&travelmode=driving`;
    Linking.openURL(url);
  }

  // CLIQUE 2: Seleciona ação e vai para fotos
  function selecionarAcao(a) {
    if (a === 'reentrega') {
      Alert.alert('Motivo da Reentrega', 'Selecione:', [
        { text: 'Cliente não estava',    onPress: () => enviarReentrega('Cliente não estava') },
        { text: 'Sem espaço no freezer', onPress: () => enviarReentrega('Sem espaço no freezer') },
        { text: 'Horário incompatível',  onPress: () => enviarReentrega('Horário incompatível') },
        { text: 'Cancelar', style: 'cancel' },
      ]);
    } else if (a === 'nao_entregue') {
      Alert.alert('Motivo da Não Entrega', 'Selecione:', [
        { text: 'Cliente ausente',         onPress: () => enviarFalha('Cliente ausente') },
        { text: 'Endereço não encontrado', onPress: () => enviarFalha('Endereço não encontrado') },
        { text: 'Recusou a entrega',       onPress: () => enviarFalha('Recusou a entrega') },
        { text: 'Cancelar', style: 'cancel' },
      ]);
    } else {
      // entregar -> vai para tela de fotos
      setAcao(a);
      setTela('fotos');
    }
  }

  async function tirarFoto(tipo) {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') { Alert.alert('Câmera necessária'); return; }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: 'images', quality: 0.5, base64: true
    });
    if (!result.canceled) {
      const asset = result.assets[0];
      if (tipo === 'outros') {
        setFotos(p => ({ ...p, outros: [...p.outros, asset] }));
      } else {
        setFotos(p => ({ ...p, canhoto: asset }));
      }
    }
  }

  // CLIQUE 3: Confirma entrega
  async function confirmarEntrega() {
    if (!fotos.canhoto) {
      Alert.alert('Foto obrigatória', 'Tire a foto do canhoto!'); return;
    }
    setLoading(true);
    try {
      const fotoB64 = fotos.canhoto.base64
        ? `data:image/jpeg;base64,${fotos.canhoto.base64}` : null;

      const res = await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({
          status: 'completed',
          ata: new Date().toISOString(),
          lat_confirmacao: gps?.latitude,
          lng_confirmacao: gps?.longitude,
          foto_base64: fotoB64,
        }),
      });

      if (res.ok) {
        if (proximoStop) {
          Alert.alert(
            '✅ Entregue!',
            `Próximo:\n#${(proximoStop.sequence||0)+1} — ${proximoStop.recipient_name}`,
            [
              { text: '🗺️ GPS', onPress: () => {
                Linking.openURL(`https://www.google.com/maps/dir/?api=1&destination=${proximoStop.lat},${proximoStop.lng}&travelmode=driving`);
                navigation.goBack();
              }},
              { text: 'OK', onPress: () => navigation.goBack() }
            ]
          );
        } else {
          Alert.alert('✅ Entregue!', 'Entrega confirmada!', [
            { text: 'OK', onPress: () => navigation.goBack() }
          ]);
        }
      } else {
        Alert.alert('Erro', 'Falha ao confirmar.');
      }
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  async function enviarReentrega(motivo) {
    setLoading(true);
    try {
      await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({ status: 'reentrega', failure_reason: motivo }),
      });
      Alert.alert('🟡 Reentrega Solicitada', 'Torre de Controle notificada.', [
        { text: 'Próximo', onPress: () => navigation.goBack() }
      ]);
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  async function enviarFalha(motivo) {
    setLoading(true);
    try {
      await fetch(`${API_URL}/routes/${routeId}/stops/${stop.stop_id}`, {
        method: 'PATCH', headers,
        body: JSON.stringify({ status: 'failed', failure_reason: motivo, atd: new Date().toISOString() }),
      });
      Alert.alert('🔴 Falha Registrada', motivo, [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (e) { Alert.alert('Erro', e.message); }
    finally { setLoading(false); }
  }

  // ─── TELA DE FOTOS (após clicar ENTREGAR) ───────────────────
  if (tela === 'fotos') {
    return (
      <Animated.View style={[s.container, { opacity: fadeAnim }]}>
        <ScrollView contentContainerStyle={s.content}>
          <Text style={s.fotoTitulo}>📸 COMPROVANTE DE ENTREGA</Text>
          <Text style={s.fotoCliente}>{stop.recipient_name}</Text>

          {/* Canhoto obrigatório */}
          <View style={s.fotoCard}>
            <Text style={s.fotoLabel}>📄 FOTO DO CANHOTO <Text style={s.obrig}>(OBRIGATÓRIA)</Text></Text>
            {fotos.canhoto ? (
              <View>
                <Image source={{ uri: fotos.canhoto.uri }} style={s.fotoPreview} />
                <TouchableOpacity style={s.btnRetake} onPress={() => tirarFoto('canhoto')}>
                  <Text style={s.btnRetakeTxt}>🔄 Tirar outra</Text>
                </TouchableOpacity>
              </View>
            ) : (
              <TouchableOpacity style={s.btnFoto} onPress={() => tirarFoto('canhoto')}>
                <Text style={{ fontSize: 40 }}>📷</Text>
                <Text style={s.btnFotoTxt}>TIRAR FOTO DO CANHOTO</Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Outras fotos */}
          <View style={s.fotoCard}>
            <Text style={s.fotoLabel}>📎 OUTRAS FOTOS <Text style={s.opcional}>(OPCIONAL)</Text></Text>
            <View style={s.outrasRow}>
              {fotos.outros.map((f, i) => (
                <Image key={i} source={{ uri: f.uri }} style={s.thumbFoto} />
              ))}
              <TouchableOpacity style={s.btnAddFoto} onPress={() => tirarFoto('outros')}>
                <Text style={{ color: '#00BFFF', fontSize: 28 }}>+</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Botão confirmar */}
          <TouchableOpacity
            style={[s.btnConfirmar, (!fotos.canhoto || loading) && { opacity: 0.4 }]}
            onPress={confirmarEntrega}
            disabled={!fotos.canhoto || loading}
          >
            {loading
              ? <ActivityIndicator color="#001020" />
              : <Text style={s.btnConfirmarTxt}>✅ FINALIZAR E PRÓXIMO</Text>
            }
          </TouchableOpacity>

          <TouchableOpacity style={s.btnVoltar} onPress={() => setTela('detalhes')}>
            <Text style={s.btnVoltarTxt}>← Voltar</Text>
          </TouchableOpacity>
        </ScrollView>
      </Animated.View>
    );
  }

  // ─── TELA 04: DETALHES DA PARADA ────────────────────────────
  return (
    <Animated.View style={[s.container, { opacity: fadeAnim }]}>
      <ScrollView contentContainerStyle={s.content}>
        {/* Cabeçalho */}
        <View style={s.header}>
          <View style={{ flex: 1 }}>
            <Text style={s.headerSeq}>PARADA #{(stop.sequence||0)+1}</Text>
            <Text style={s.headerNome}>{stop.recipient_name}</Text>
            <Text style={s.headerCod}>COD SANKHYA: {stop.codparc||'—'}</Text>
            <Text style={s.headerEnd} numberOfLines={2}>{stop.address}</Text>
          </View>
          <TouchableOpacity style={s.btnMaps} onPress={abrirMaps}>
            <Text style={{ fontSize: 24 }}>🗺️</Text>
            <Text style={s.btnMapsTxt}>GPS</Text>
          </TouchableOpacity>
        </View>

        {/* KPIs */}
        <View style={s.kpiRow}>
          <View style={s.kpi}>
            <Text style={s.kpiVal}>{(stop.weight_kg||0).toFixed(0)}</Text>
            <Text style={s.kpiLbl}>kg total</Text>
          </View>
          <View style={s.kpi}>
            <Text style={s.kpiVal}>{notas.length}</Text>
            <Text style={s.kpiLbl}>notas</Text>
          </View>
          <View style={s.kpi}>
            <Text style={s.kpiVal}>{stop.eta||'--:--'}</Text>
            <Text style={s.kpiLbl}>ETA</Text>
          </View>
        </View>

        {/* Lista de notas */}
        <View style={s.notasCard}>
          <Text style={s.notasLabel}>📄 NOTAS / PEDIDOS</Text>
          {loadNotas ? (
            <ActivityIndicator color="#00BFFF" style={{ marginTop: 12 }} />
          ) : notas.length === 0 ? (
            <Text style={s.semNotas}>Nenhuma nota encontrada</Text>
          ) : (
            notas.map((nota, i) => (
              <View key={i} style={s.notaItem}>
                <View style={s.notaHeader}>
                  <Text style={s.notaNum}>📋 Nota {nota.external_id}</Text>
                  <View style={s.topBadge}>
                    <Text style={s.topBadgeTxt}>
                      TOP {nota.top_app} — {TOP_LABEL[nota.top_app] || nota.top_app}
                    </Text>
                  </View>
                </View>
                {(nota.itens||[]).map((item, j) => (
                  <View key={j} style={s.itemRow}>
                    <Text style={s.itemNome}>• {item.nome || NOME_ITEM[item.cod] || item.cod}</Text>
                    <Text style={s.itemQtd}>{item.qtd} un</Text>
                  </View>
                ))}
                <Text style={s.notaPeso}>⚖️ {nota.weight_kg?.toFixed(0)||0} kg</Text>
              </View>
            ))
          )}
        </View>

        {/* Botões de ação - GRANDES e coloridos */}
        <View style={s.acoesRow}>
          <TouchableOpacity style={s.btnEntregar} onPress={() => selecionarAcao('entregar')}>
            <Text style={s.btnAcaoEmoji}>✅</Text>
            <Text style={s.btnAcaoTxt}>ENTREGAR</Text>
          </TouchableOpacity>
        </View>
        <View style={s.acoesRow}>
          <TouchableOpacity style={s.btnReentrega} onPress={() => selecionarAcao('reentrega')}>
            <Text style={s.btnAcaoEmoji}>🟡</Text>
            <Text style={[s.btnAcaoTxt, { color: '#001020' }]}>REENTREGA</Text>
          </TouchableOpacity>
          <TouchableOpacity style={s.btnNaoEntregue} onPress={() => selecionarAcao('nao_entregue')}>
            <Text style={s.btnAcaoEmoji}>🔴</Text>
            <Text style={s.btnAcaoTxt}>NÃO ENTREGUE</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </Animated.View>
  );
}

const s = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#001020' },
  content: { padding: 16, gap: 12, paddingBottom: 40 },
  // Header
  header: { backgroundColor: 'rgba(0,30,60,0.95)', borderRadius: 16, padding: 16, flexDirection: 'row', gap: 12, borderWidth: 1, borderColor: 'rgba(0,191,255,0.25)' },
  headerSeq: { color: '#00BFFF', fontSize: 10, fontWeight: '800', letterSpacing: 3, marginBottom: 4 },
  headerNome: { color: '#fff', fontSize: 18, fontWeight: '900', marginBottom: 2 },
  headerCod: { color: '#00BFFF', fontSize: 11, fontWeight: '600', marginBottom: 4 },
  headerEnd: { color: 'rgba(255,255,255,0.4)', fontSize: 11, lineHeight: 16 },
  btnMaps: { width: 56, height: 56, borderRadius: 12, backgroundColor: 'rgba(0,191,255,0.15)', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: 'rgba(0,191,255,0.3)', gap: 2 },
  btnMapsTxt: { color: '#00BFFF', fontSize: 9, fontWeight: '700' },
  // KPIs
  kpiRow: { flexDirection: 'row', gap: 8 },
  kpi: { flex: 1, backgroundColor: 'rgba(0,30,60,0.8)', borderRadius: 10, padding: 12, alignItems: 'center', borderWidth: 1, borderColor: 'rgba(0,191,255,0.15)' },
  kpiVal: { color: '#00BFFF', fontSize: 22, fontWeight: '900' },
  kpiLbl: { color: 'rgba(255,255,255,0.4)', fontSize: 10, marginTop: 2 },
  // Notas
  notasCard: { backgroundColor: 'rgba(0,30,60,0.95)', borderRadius: 16, padding: 14, borderWidth: 1, borderColor: 'rgba(0,191,255,0.15)' },
  notasLabel: { color: '#00BFFF', fontSize: 10, fontWeight: '800', letterSpacing: 2, marginBottom: 10 },
  semNotas: { color: 'rgba(255,255,255,0.3)', fontSize: 12, textAlign: 'center', padding: 12 },
  notaItem: { backgroundColor: 'rgba(0,10,30,0.5)', borderRadius: 10, padding: 10, marginBottom: 8, borderWidth: 1, borderColor: 'rgba(0,191,255,0.1)' },
  notaHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 },
  notaNum: { color: '#fff', fontSize: 12, fontWeight: '700' },
  topBadge: { backgroundColor: 'rgba(0,191,255,0.15)', borderRadius: 6, paddingHorizontal: 8, paddingVertical: 3, borderWidth: 1, borderColor: 'rgba(0,191,255,0.3)' },
  topBadgeTxt: { color: '#00BFFF', fontSize: 10, fontWeight: '700' },
  itemRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 2 },
  itemNome: { color: 'rgba(255,255,255,0.6)', fontSize: 11 },
  itemQtd: { color: '#00BFFF', fontSize: 11, fontWeight: '700' },
  notaPeso: { color: 'rgba(255,255,255,0.35)', fontSize: 10, marginTop: 4 },
  // Ações
  acoesRow: { flexDirection: 'row', gap: 10 },
  btnEntregar: { flex: 1, backgroundColor: '#00FF88', borderRadius: 14, padding: 18, alignItems: 'center' },
  btnReentrega: { flex: 1, backgroundColor: '#FFD700', borderRadius: 14, padding: 18, alignItems: 'center' },
  btnNaoEntregue: { flex: 1, backgroundColor: '#FF3355', borderRadius: 14, padding: 18, alignItems: 'center' },
  btnAcaoEmoji: { fontSize: 28, marginBottom: 4 },
  btnAcaoTxt: { color: '#fff', fontWeight: '900', fontSize: 13, letterSpacing: 1 },
  // Tela fotos
  fotoTitulo: { color: '#00BFFF', fontSize: 12, fontWeight: '800', letterSpacing: 2, textAlign: 'center' },
  fotoCliente: { color: '#fff', fontSize: 16, fontWeight: '900', textAlign: 'center', marginBottom: 8 },
  fotoCard: { backgroundColor: 'rgba(0,30,60,0.95)', borderRadius: 16, padding: 14, borderWidth: 1, borderColor: 'rgba(0,191,255,0.15)' },
  fotoLabel: { color: '#00BFFF', fontSize: 10, fontWeight: '800', letterSpacing: 2, marginBottom: 10 },
  obrig: { color: '#FF3355' },
  opcional: { color: 'rgba(255,255,255,0.4)' },
  btnFoto: { borderWidth: 1.5, borderColor: 'rgba(0,191,255,0.3)', borderStyle: 'dashed', borderRadius: 12, padding: 28, alignItems: 'center', gap: 8 },
  btnFotoTxt: { color: '#00BFFF', fontWeight: '800', fontSize: 12, letterSpacing: 1 },
  fotoPreview: { width: '100%', height: 200, borderRadius: 10 },
  outrasRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  thumbFoto: { width: 80, height: 80, borderRadius: 8 },
  btnAddFoto: { width: 80, height: 80, borderRadius: 8, borderWidth: 1.5, borderColor: 'rgba(0,191,255,0.3)', borderStyle: 'dashed', alignItems: 'center', justifyContent: 'center' },
  btnRetake: { padding: 10, alignItems: 'center' },
  btnRetakeTxt: { color: '#00BFFF', fontSize: 12, fontWeight: '600' },
  btnConfirmar: { backgroundColor: '#00FF88', borderRadius: 14, padding: 18, alignItems: 'center' },
  btnConfirmarTxt: { color: '#001020', fontWeight: '900', fontSize: 15, letterSpacing: 2 },
  btnVoltar: { padding: 14, alignItems: 'center' },
  btnVoltarTxt: { color: 'rgba(255,255,255,0.4)', fontSize: 13 },
});
"""

with open(r'C:\gelocrim-motorista\screens\EntregaScreen.js', 'w', encoding='utf-8') as f:
    f.write(conteudo)
print('EntregaScreen.js (Tela 04) reescrito!')
